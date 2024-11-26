A model inversion challenge.
Solution code in `soln/`
Concept:
1. Attach another model to the inputs of the original model
2. Freeze the params of the original model
3. Train the attacker model to generate sth that makes original model say "ok accepted"
4. Remove the original model, get outputs of attacker model, and you can see the image used to train
5. Repeat for all 6 numbers, great success

Flag: `blahaj{246748}`