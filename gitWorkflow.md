# Git and GitHub Workflow

## Key ideas

- A **branch** is a separate line of work in your project.
- The `main` branch holds the stable version of the code.
- Do not change `main` directly. Make a new branch for each task.
- A **commit** is a save point on a branch.
- `git status` does not contact GitHub. It uses a local copy of the remote data.
- `git fetch` gets new data from GitHub. It does not change your files.
- `git pull` does a fetch and then a merge on the current branch.

---

## Step 1: Start from the latest main

```
git switch main                  # go to the main branch
git pull                         # get the latest changes from GitHub
```

---

## Step 2: Go to a branch (choose Option A or Option B)

### Option A: Make a new branch

Use this for a new task. Your work stays separate from the work of other people.

```
git switch -c branchname         # -c means "create". Git makes the branch and goes to it
git status                       # the first line shows the name of the current branch
```

### Option B: Use a branch that already exists

Use this to continue your own work, or to add to the work of a team member. Ask the team member first. Two people on one branch can cause conflicts.

```
git fetch                        # get the latest branch data from GitHub
git switch branchname            # go to the branch
git pull                         # get the latest commits on this branch
```

---

## Step 3: Change files and commit

Change your files in VS Code. Then run these commands:

```
git status                       # shows which files changed
git diff                         # shows the changes in the files
git add filename                 # adds one file (use this more often)
git add .                        # adds all changes in this folder and its subfolders
git commit -m "message"          # saves the changes. Write a short description
```

You can make many commits on the same branch.

---

## Step 4: Push the branch to GitHub

```
git push -u origin branchname    # Option A only: first push. -u links your branch to GitHub
git push                         # Option B, and all next pushes in Option A
```

---

## Step 5: Make a pull request on GitHub

1. Open your repository on GitHub.
2. Click **Compare & pull request**.
3. Write a short description of your change.
4. Click **Create pull request**.
5. A team member reviews your work.
6. Click **Merge pull request**. GitHub merges your branch into `main`.

---

## Step 6: Clean up on your computer

```
git switch main                  # go back to main
git pull                         # get the merged work from GitHub
git branch -d branchname         # delete the old local branch
```

For the next task, go back to Step 1.

---

## Other cases

### A. Main changes while you work on your branch

```
git switch main                  # go to main
git pull                         # get the latest changes
git switch branchname            # go back to your branch
git merge main                   # put the changes from main into your branch
```

### B. A team member makes a new branch

```
git fetch                        # get the new branch data from GitHub
git branch -r                    # show the remote branches
git switch branchname            # go to the new branch
```

### C. A team member pushes new commits to your branch

```
git switch branchname            # go to the branch
git pull                         # get the new commits
```

---

## Notes

- Commit your changes before you switch to a different branch.
- `git switch` changes the files in VS Code to match the branch.
- Each branch has its own version of the files. `main` does not hold all branches.
- Do not add secret keys or private files. Put them in a `.gitignore` file.
- For work alone on a small project, you can skip the pull request.