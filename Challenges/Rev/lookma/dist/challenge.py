(e:=[ord(c)-46 for c in input("What's the flag? ")],o:="".join(chr(sum((e[i]*(5**f)**i)for i in range(len(e)))%79+46)for f in range(len(e))),print(["Nope, try again.","You got it!"][o==r"OjyF9Sr@JdtZLTp7efyD`ZzQ9gS]x7\=iMM"]))