# CI/CD Definition

CI/CD stands for **Continuous Integration** and **Continuous Delivery/Deployment**. It is the automated assembly line of modern software development.

In plain English: **CI/CD is a robot that automatically tests your code when you push it, and then automatically deploys it to production if the tests pass.**

Let's break down the two halves.

### **1. CI: Continuous Integration (The Quality Control)**

"Integration" means merging your code with the rest of the team's code. "Continuous" means doing it frequently, usually multiple times a day.

When a developer pushes code to GitHub, the CI pipeline (a robot) wakes up and runs a series of automated checks:

- **Linting:** Is the code formatted correctly?
- **Unit Tests:** Do the functions work as expected?
- **Build:** Does the code compile/package correctly?

If any of these fail, the CI pipeline stops and emails the developer: *"Your code broke something. Fix it before we go further."* This prevents broken code from ever reaching production.

### **2. CD: Continuous Delivery/Deployment (The Shipping Robot)**

Once the CI tests pass, the CD pipeline takes over. It handles the "shipping" of the code.

- **Continuous Delivery:** The robot prepares the deployment (builds the Docker image, updates the `prefect.yaml`) but stops short of actually releasing it. A human has to click a button to say "Go live."
- **Continuous Deployment:** The robot does everything automatically. No human button. The moment tests pass, the new version is live in production.

### **The Analogy: The Restaurant Chain**

Let's go back to our restaurant chain analogy:

- **CI (The Quality Control Kitchen):** A chef invents a new recipe (writes code). Before it goes on the menu, the QC kitchen (CI robot) tests it. Does it taste good? Are the ingredients safe? (Unit tests). If it's bad, the recipe is rejected.
- **CD (The Distribution Network):** Once the recipe passes QC, the distribution network (CD robot) automatically prints the new menu, updates the website, and emails all the restaurant managers to say: "New dish available. Update your menus."

### **How CI/CD Connects to Prefect**

Remember when I said: *"CI/CD runs `prefect deploy --all` automatically"*?

Here is exactly how that works in practice using a tool like **GitHub Actions**:

1. **A developer pushes code to GitHub.** They made a change to `my_pipeline.py` or added a new deployment to `prefect.yaml`.
2. **GitHub Actions notices the push.** This is the CI/CD robot. It spins up a temporary, isolated virtual machine (called a "runner") in the cloud.
3. **The runner installs Python and Prefect.** It runs `pip install prefect`.
4. **The runner authenticates with the Prefect API.** It uses a secret API key stored securely in GitHub's settings to log in to your Prefect Cloud or Self-Hosted server.
5. **The runner executes the deployment command.** It runs `prefect deploy --all`.
6. **The deployment is registered.** The Prefect API updates the blueprint in the database.
7. **The runner shuts down.** It deletes itself. The whole process took 30 seconds.

### **Why Teams Use CI/CD**

Without CI/CD, deploying is a manual, error-prone process:

- "Hey, did you remember to run the tests?"
- "Oops, I forgot to update the schedule in the YAML."
- "It works on my machine, but not on the server."

With CI/CD:

- Every change is tested automatically.
- Every deployment is registered automatically.
- The process is consistent, repeatable, and documented in the CI/CD config file (e.g., `.github/workflows/deploy.yml`).

### **The Full Picture**

Here is how the whole production stack fits together:

text

```
Developer writes code
       ↓
Pushes to GitHub
       ↓
CI/CD Robot (GitHub Actions) wakes up
       ↓
Runs tests (CI)
       ↓
Runs `prefect deploy --all` (CD)
       ↓
Prefect API registers the deployment
       ↓
Worker (already running 24/7) picks up the run
       ↓
Flow executes
```

The developer never manually types `prefect deploy`. The robot does it for them, every time they push code. That is the power of CI/CD