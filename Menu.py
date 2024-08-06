import os
print('欢迎使用FQ Toolbox V1.2')
while True:
    choose = input('1.搜索书籍\n2.阅读书籍\n3.爬取书籍\n请选择:')
    if choose == '1':
        os.system('python ./FQSearch.py')
    elif choose == '2':
        os.system('python ./FQread.py')
    elif choose == '3':
        os.system('python ./FQ爬虫.py')
    else:
        print('unknown')
    
