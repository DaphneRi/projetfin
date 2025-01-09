def ans_verif(a):
  note=20
  v=list(input("Quelles sont les bonnes reponses du sujet ?"))
  r=list(a)
  for x in len(v):
    if r[x]!=v[x]:
      note=note-2.5
    else:
      note=note
    print(note)
      
