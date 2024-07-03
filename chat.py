import ollama
import re

item = 'electric screwdriver'
rows = []


modelfile = '''
FROM llama3
SYSTEM Any content generated should be as concise as possible, no more than 10 words.
PARAMETER temperature 0.5
'''
ollama.create(model='fmea_analyzer', modelfile=modelfile)

opt = dict(seed=10)

itemPrompt = [
    {
        'role':'user',
        'content':f'What are the components of a {item}. Only give the name of the component, one on each line. Remove any quotation marks.',
    },
]

response = ollama.chat('fmea_analyzer', messages=itemPrompt, options=opt)

components = response['message']['content'].split('\n')
# print(components)

for c in components: #get possible failure modes

    fMPrompt = [
        {
            'role':'user',
            'content':f'What are one or two ways a {c} in a {item} could fail? Failures can range from catastrophic to minor and unnoticeable. Format the output as a list with one failure mode on its own separate line. Do NOT say anything before or after this.',
        },
    ]

    r = ollama.chat('fmea_analyzer', messages=fMPrompt, options=opt)
    
    formatted = r['message']['content'].split('\n')
    # print(formatted)
    
    for i in formatted:
        if i: #sometimes the models will spit out extra whitespace and this needs to be trimmed
            rows.append([c, i])

# for r in rows:
#     print(r)

for idx, r in enumerate(rows):
    component = r[0] #component always comes first
    fm = r[1] #associated failure mode with component
    
    effectPrompt = [
        {
            'role':'user',
            'content':f'What is a potential effect of a {component} in a {item} failing due to {fm}? Do NOT say anything before or after this.',
        },
    ]

    effects = ollama.chat('fmea_analyzer', messages=effectPrompt, options=opt)['message']['content']

    severityPrompt = [
        {
            'role':'user',
            'content':f'Given that the {component} of a {item} fails due to {fm} and this causes {effects}, assign a score that measure the severity of the failure and its effects from 1-10, with 1 meaning the {item} still functions and 10 meaning the {item} does not function and poses significant safety risks. Do NOT say anything before or after this.',
        },
    ]

    severity = ollama.chat('fmea_analyzer', messages=severityPrompt, options=opt)['message']['content']
    severity = re.sub('[^0-9]','', severity)

    rows[idx] = [component, fm, effects, severity]



f = open('result.csv', 'w')

for r in rows: #write components to csv
    for item in r:
        f.write(item + ",")
    f.write('\n')