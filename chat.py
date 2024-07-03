import ollama

item = 'electric screwriver'
rows = []

modelfile = '''
FROM llama3
SYSTEM Format all responses as CSV with one element on each line. Do not generate input beyond this. Any content generated should be as concise as possible, no more than 10 words.
PARAMETER temperature 0
'''
ollama.create(model='fmea_analyzer', modelfile=modelfile)
response = ollama.generate(model='fmea_analyzer', prompt=f'What are the components of a {item}. Only give the name of the component. Remove any quotation marks.')

components = response['response'].split('\n')

for c in components: #get possible failure modes
    r = ollama.generate(model='fmea_analyzer', prompt=f'What are one or two ways a {c} in a {item} could fail. Separate ways it can fail onto different lines. Remove any quotation marks.')
    
    formatted = r['response'].split('\n')
    print(formatted)
    
    for item in formatted:
        rows.append([c, item])

# for r in rows:
#     print(r)
# f = open('result.csv', 'w')

# for c in components: #write components to csv
#     f.write(c + ",")