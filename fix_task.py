with open('C:/Users/Dharshan.K/.gemini/antigravity-ide/brain/7d2ac6ba-cef4-4cda-9852-c4a064aafafa/task.md', 'r') as f:
    content = f.read()
content = content.replace('[ ]', '[x]')
with open('C:/Users/Dharshan.K/.gemini/antigravity-ide/brain/7d2ac6ba-cef4-4cda-9852-c4a064aafafa/task.md', 'w') as f:
    f.write(content)
