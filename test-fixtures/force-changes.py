import filecmp
  
f1 = "file.txt"
f2 = "file2.txt"
  
# shallow comparison
result = filecmp.cmp(f1, f2)
print(result)
# deep comparison
result = filecmp.cmp(f1, f2, shallow=False)
print(result)

with open("file2.txt", "a") as f:
     f.write("new line\n")