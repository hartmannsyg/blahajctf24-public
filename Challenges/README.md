## How to add your challenges

Create a folder with the name of your challenge (be creative)

Folder structure example:
```
challengename
- src
- - server.py
- - Dockerfile
- dist
- - server.py
- - Dockerfile
- solution.md
- challenge.yml
```

The `src` folder contains everything that goes into the creation of challenges like Dockerfile, server file, Makefile, etc ...

The `dist` folder contains everything that is given to the players as source code (rmb to remove flags)

The `solution.md` contains method to solve (pls be elaborate)

The `challenge.yml` contains the Author name, Challenge name, Description, Hint (if any), Category, Difficulty, Points.
It follows the CTFd format found [here](https://github.com/CTFd/ctfcli/blob/master/ctfcli/spec/challenge-example.yml)
