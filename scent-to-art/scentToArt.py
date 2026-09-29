# Step 1 - imports
import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import anthropic
from dotenv import load_dotenv

print("All imports successful!")

# Step 2 - load data
url = "https://raw.githubusercontent.com/pyrfume/pyrfume-data/main/leffingwell/behavior.csv"
data = pd.read_csv(url)
print(data.head())
print(data.shape)

# Step 3 - set up API connection
load_dotenv(override=True)
key = os.getenv("ANTHROPIC_API_KEY")
print(f"Key being used: {key[:20]}")
client = anthropic.Anthropic(api_key=key)

# Toggle self-reports on/off to control token cost
ENABLE_SELF_REPORTS = False

descriptor_columns = data.columns[1:]  # skip 'Stimulus' column


def get_descriptors(row):
    return [col for col in descriptor_columns if row[col] == 1]


# ============================================================
# Step 4 - Select 5 random molecules from the dataset
# ============================================================
SAMPLE_SIZE = 5
sample_molecules = data.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

print(f"\nSelected {SAMPLE_SIZE} random molecules:")
for i, row in sample_molecules.iterrows():
    print(f"  {i+1}. ID {row['Stimulus']} -> {get_descriptors(row)}")


# ============================================================
# GENERATIVE AGENT 1: Synthetic Agent (searches internet ONCE, batched)
# ============================================================
def synthetic_agent_search(all_descriptors_union, client, model="claude-sonnet-4-5"):
    try:
        prompt = f"""Search for scientific or perfumery information about molecules 
with these odor descriptors: {', '.join(all_descriptors_union)}. 
Summarize any relevant chemical or structure-odor relationship context in 3-4 sentences."""

        response = client.messages.create(
            model=model,
            max_tokens=250,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": prompt}]
        )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        result = " ".join(text_blocks) if text_blocks else "No additional context found."
        print("Synthetic Agent (web search) succeeded.")
        return result

    except Exception as e:
        print(f"Synthetic Agent web search unavailable ({e}). Falling back to dataset cross-reference...")
        try:
            fallback_url = "https://raw.githubusercontent.com/pyrfume/pyrfume-data/main/dravnieks/behavior.csv"
            extra_data = pd.read_csv(fallback_url)
            return f"Cross-referenced fallback dataset with {extra_data.shape[0]} molecules (no live web data available)."
        except Exception as e2:
            return "No additional grounding context available."


all_descriptors_seen = set()
for _, row in sample_molecules.iterrows():
    all_descriptors_seen.update(get_descriptors(row))

search_context = synthetic_agent_search(list(all_descriptors_seen), client)
print(f"\n🔎 SYNTHETIC AGENT CONTEXT:\n{search_context}")


# ============================================================
# EMPIRICAL AGENT 1: Augmentation Agent
# Proposes ONE structural modification (in plain language)
# ============================================================
def augmentation_agent(molecule_id, original_descriptors, client, model="claude-sonnet-4-5"):
    prompt = f"""You are a molecular structure augmentation agent.

A molecule (ID: {molecule_id}) has known odor descriptors: {', '.join(original_descriptors)}.
We do not have its exact structure, but based on these descriptors, infer a plausible 
chemical structural class (e.g., ester, aldehyde, terpene, alcohol).

Propose ONE plausible structural modification to this molecule 
(e.g., "replace a hydroxyl group with a methyl group", "add a double bond", 
"lengthen the carbon chain by two units", "replace an ester with an aldehyde group").

Respond in EXACTLY this format, nothing else:
INFERRED_CLASS: [chemical class]
MODIFICATION: [one sentence describing the structural change]
"""
    response = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text.strip()
    lines = text.split("\n")

    inferred_class = next((l.split(":", 1)[1].strip() for l in lines if l.upper().startswith("INFERRED_CLASS")), "unknown")
    modification = next((l.split(":", 1)[1].strip() for l in lines if l.upper().startswith("MODIFICATION")), text)

    self_report = None
    if ENABLE_SELF_REPORTS:
        report_prompt = f"""You are the Augmentation Agent. You just proposed this structural change 
to molecule {molecule_id} (inferred class: {inferred_class}): {modification}

Write a brief first-person paragraph (2-3 sentences) explaining your reasoning. Speak as "I"."""
        report_response = client.messages.create(
            model=model, max_tokens=120,
            messages=[{"role": "user", "content": report_prompt}]
        )
        self_report = report_response.content[0].text.strip()

    return inferred_class, modification, self_report


# ============================================================
# EMPIRICAL AGENT 2: Evaluator Agent
# Predicts a FULL descriptor set for the modified molecule
# ============================================================
def evaluator_agent(molecule_id, original_descriptors, inferred_class, modification, search_context, client, model="claude-sonnet-4-5"):
    prompt = f"""You are an expert olfactory chemist predicting scent profiles from structural changes.

Original molecule (ID: {molecule_id}), inferred class: {inferred_class}
Original odor descriptors: {', '.join(original_descriptors)}

Proposed structural modification: {modification}

Real-world grounding context (from research/search):
{search_context}

Based on the original descriptors, the structural modification, and the grounding context,
predict the FULL set of odor descriptors (3-6 descriptors) you would expect for the 
MODIFIED molecule. Some may overlap with the original; some should be new.

Respond ONLY with a comma-separated list of descriptors. No explanation, no extra text.
"""
    response = client.messages.create(
        model=model,
        max_tokens=60,
        messages=[{"role": "user", "content": prompt}]
    )
    raw_text = response.content[0].text.strip()
    predicted_descriptors = [d.strip() for d in raw_text.split(",") if d.strip()]

    self_report = None
    if ENABLE_SELF_REPORTS:
        report_prompt = f"""You are the Evaluator Agent. You just predicted the descriptor set 
{predicted_descriptors} for a modified version of molecule {molecule_id} 
(original: {original_descriptors}, modification: {modification}).

Write a brief first-person paragraph (2-3 sentences) explaining how you weighed the original 
descriptors, the structural change, and the search context to reach this prediction. Speak as "I"."""
        report_response = client.messages.create(
            model=model, max_tokens=120,
            messages=[{"role": "user", "content": report_prompt}]
        )
        self_report = report_response.content[0].text.strip()

    return predicted_descriptors, self_report


# ============================================================
# SUPERVISOR AGENT: simple call-budget circuit breaker
# ============================================================
class SupervisorAgent:
    def __init__(self, max_calls=30):
        self.max_calls = max_calls
        self.call_count = 0

    def log_call(self, label=""):
        self.call_count += 1
        print(f"[Supervisor] API call #{self.call_count} {('- ' + label) if label else ''}")
        if self.call_count > self.max_calls:
            print("[Supervisor] ⛔ Call budget exceeded - halting to prevent runaway cost.")
            return False
        return True


supervisor = SupervisorAgent(max_calls=30)


# ============================================================
# MAIN LOOP: process all 5 sampled molecules
# ============================================================
original_results = []
augmented_results = []

for i, row in sample_molecules.iterrows():
    molecule_id = row['Stimulus']
    original_descriptors = get_descriptors(row)

    print(f"\n===== Molecule {i+1}/{SAMPLE_SIZE}: ID {molecule_id} =====")
    print(f"Original descriptors: {original_descriptors}")
    original_results.append({"id": molecule_id, "descriptors": original_descriptors})

    if not supervisor.log_call("augmentation"):
        break
    inferred_class, modification, aug_report = augmentation_agent(molecule_id, original_descriptors, client)
    print(f"🧬 Augmentation Agent -> class: {inferred_class} | modification: {modification}")
    if aug_report:
        print(f"🧬 AUGMENTATION REPORT:\n{aug_report}")

    if not supervisor.log_call("evaluator"):
        break
    predicted_descriptors, eval_report = evaluator_agent(
        molecule_id, original_descriptors, inferred_class, modification, search_context, client
    )
    print(f"⚖️ Evaluator Agent predicted descriptors: {predicted_descriptors}")
    if eval_report:
        print(f"⚖️ EVALUATOR REPORT:\n{eval_report}")

    augmented_results.append({
        "id": molecule_id,
        "inferred_class": inferred_class,
        "modification": modification,
        "predicted_descriptors": predicted_descriptors
    })


# ============================================================
# Print all 10 lists clearly
# ============================================================
print("\n\n========== FINAL RESULTS: 10 LISTS ==========")
for i in range(SAMPLE_SIZE):
    print(f"\n--- List {2*i+1}: ORIGINAL molecule {original_results[i]['id']} ---")
    print(original_results[i]['descriptors'])

    print(f"\n--- List {2*i+2}: AUGMENTED molecule {augmented_results[i]['id']} "
          f"({augmented_results[i]['modification']}) ---")
    print(augmented_results[i]['predicted_descriptors'])


# ============================================================
# GENERATIVE AGENT 2: Visual Agent - 5x2 comparison grid
# ============================================================
def draw_scent_diagram(ax, label, original_descriptors, comparison_descriptors):
    """Draws one radial diagram on a given matplotlib axis.
    Nodes present in BOTH original and comparison are gold (shared).
    Nodes only in comparison (new) are magenta.
    """
    all_nodes = list(dict.fromkeys(original_descriptors + comparison_descriptors))  # unique, ordered
    n = len(all_nodes)
    if n == 0:
        ax.axis("off")
        return

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 3
    positions = {node: (radius * np.cos(a), radius * np.sin(a)) for node, a in zip(all_nodes, angles)}
    center = (0, 0)

    for node in all_nodes:
        x, y = positions[node]
        is_new = node not in original_descriptors
        color = "#ff2ec4" if is_new else "#ffd700"
        for width, alpha in [(5, 0.06), (3, 0.15), (1.5, 0.5)]:
            ax.plot([center[0], x], [center[1], y], color=color, linewidth=width, alpha=alpha, zorder=1)

    for size, alpha in [(1500, 0.15), (700, 0.4), (300, 1)]:
        ax.scatter(*center, s=size, color="white", alpha=alpha, zorder=2)

    for node in all_nodes:
        x, y = positions[node]
        is_new = node not in original_descriptors
        color = "#ff2ec4" if is_new else "#ffd700"
        for size, alpha in [(600, 0.2), (300, 1)]:
            ax.scatter(x, y, s=size, color=color, alpha=alpha, zorder=3)
        ax.text(x * 1.3, y * 1.3, node, color="white", fontsize=8,
                 ha="center", va="center", zorder=4)

    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(label, color="white", fontsize=10, pad=10)


def visualize_all_molecules(original_results, augmented_results):
    plt.style.use("dark_background")
    fig, axes = plt.subplots(SAMPLE_SIZE, 2, figsize=(10, 5 * SAMPLE_SIZE), facecolor="black")

    for i in range(SAMPLE_SIZE):
        orig = original_results[i]
        aug = augmented_results[i]

        draw_scent_diagram(
            axes[i][0],
            f"Original\nID {orig['id']}",
            orig['descriptors'], orig['descriptors']
        )
        draw_scent_diagram(
            axes[i][1],
            f"Augmented ({aug['inferred_class']})\nID {aug['id']}",
            orig['descriptors'], aug['predicted_descriptors']
        )

    fig.suptitle("Scent Neural Map: Original vs. Augmented Molecules",
                 color="white", fontsize=16, y=0.995)
    plt.tight_layout()
    plt.savefig("scent_network_grid.png", dpi=150, facecolor="black")
    plt.show()
    print("\nVisualization saved as scent_network_grid.png")


visualize_all_molecules(original_results, augmented_results)