[README.md](https://github.com/user-attachments/files/32588169/README.md)
# Kyle Robin: Portfolio

**Live site:** https://krobin2005.github.io/myportfolio/

My personal portfolio, built for **DCS340** at Bates College. I'm a Digital & Computational Sciences and Psychology double major, the lead of AI research in Professor Jason Castro's neuroscience lab, and an NCAA Division I alpine skier.

The site is hand-coded in HTML, CSS, and vanilla JavaScript and hosted with GitHub Pages. It has no frameworks and no build step.

## What's on the site

- **About:** who I am and what pulls me between computing and the mind
- **Experience:** AI research, the Bates Investment Club, and the BMA solar energy proposal
- **Projects:** the Digital Olfaction Agent, the BMA Solar Feasibility Study, industrial equity pitches, and this site
- **Learning Log:** my work from the DCS340 optimization module, with links to the Colab notebooks and code
- **Athletics:** D1 skiing at Bates and international FIS racing
- **Skills and contact**

## DCS340 Optimization Module

The `dcs340/` folder holds my explorations from *Introduction to Classical Methods in Optimization*:

| File | What it does |
|---|---|
| `optimization_method_experimentation___homework_dcs340___sep_16,_2026.py` | **The Pumpkin Problem.** Finds the peak of a launched pumpkin's path with bisection and with Newton's method, then compares the two. |
| `2d_input_(3d_objects)_opptimization_intro.py` | **Finding the Bottom of the Bowl.** Minimizes a 2D paraboloid with Nelder–Mead, Newton's method (hand-derived gradient and Hessian), and my own gradient descent. |
| `torus.py` / `torus.png` | **Building a Torus.** Generates and renders a parametric 3D surface with NumPy and Matplotlib. |
| `optimizationIntroduction.py` | An early bisection-method sketch (in progress). |

The Python files were exported from Google Colab. Each one lists its original notebook link at the top.

## Repo structure

```
myportfolio/
├── index.html     # page content and structure
├── style.css      # layout, colors, and responsive design
├── script.js      # mobile menu, scroll animations, active nav link
├── images/        # photos used on the site
└── dcs340/        # optimization module code and figures
```

## Running it locally

Clone the repo and open `index.html` in any browser:

```bash
git clone https://github.com/krobin2005/myportfolio.git
cd myportfolio
open index.html
```

## Built with

HTML, CSS, JavaScript, GitHub Pages, and Claude as a coding assistant.

## Contact

krobin@bates.edu · [LinkedIn](https://www.linkedin.com/in/kyle-robin-931415425/) · [GitHub](https://github.com/krobin2005)
