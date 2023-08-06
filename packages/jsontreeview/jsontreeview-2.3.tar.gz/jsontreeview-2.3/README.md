# JsonTreeView
  A simple python program for viewing JSON data more clearly
  
 # How to use
  ```py
  from jsontreeview import treeView
  ...
  # Works for both dict and list types
  treeView(obj, output="out.txt") # optional output file argument, default is stdout
```

# Example
  Input:
  ```json
  {"glossary":{"title":"exampleglossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"StandardGeneralizedMarkupLanguage","Acronym":"SGML","Abbrev":"ISO8879:1986","GlossDef":{"para":"Ameta-markuplanguage,usedtocreatemarkuplanguagessuchasDocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}
  ```
  Output:
  ```txt
  ["glossary"]:
   -["title"]: str
   -["GlossDiv"]:
    --["title"]: str
    --["GlossList"]:
     ---["GlossEntry"]:
      ----["ID"]: str
      ----["SortAs"]: str
      ----["GlossTerm"]: str
      ----["Acronym"]: str
      ----["Abbrev"]: str
      ----["GlossDef"]:
       -----["para"]: str
       -----["GlossSeeAlso"]:
        ----->[0]: str
        ----->[1]: str
      ----["GlossSee"]: str
  ```
