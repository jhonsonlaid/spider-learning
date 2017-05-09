from bs4 import BeautifulSoup

f_list_html = 'h-list.html'
soup = BeautifulSoup(open(f_list_html), "lxml")

print """
    :::::::::   ::::::::  :::    ::: :::   ::: :::    :::
    :+:    :+: :+:    :+: :+:    :+: :+:   :+: :+:    :+:
    +:+    +:+ +:+    +:+ +:+    +:+  +:+ +:+  +:+    +:+
    +#+    +:+ +#+    +:+ +#+    +:+   +#++:   +#+    +:+
    +#+    +#+ +#+    +#+ +#+    +#+    +#+    +#+    +#+
    #+#    #+# #+#    #+# #+#    #+#    #+#    #+#    #+#
    #########   ########   ########     ###     ########
    """
for index, fl in enumerate(soup.find_all('li')):
    ftitle = fl.find("a", target=True)
    ftime = fl.find("a", class_="head-ico4")
    fname = fl.find("a", class_="head-ico2")
    froom = fl.find("a", class_="head-ico3")
    print ("\n----------- " + str(index) + " "
           + fname.get_text()
           + " ------------")
    if ftime:
        print ftime.get_text(), ftitle.get_text().encode("gb18030")
    else:
        print ftitle.get_text().encode("gb18030")