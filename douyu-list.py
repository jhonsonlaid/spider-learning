from bs4 import BeautifulSoup

f_list_html = 'h-list.html'


def get_douyu_list(f_list_html):
    soup = BeautifulSoup(open(f_list_html), "lxml")
    print("""
           ___   ____   __  __ __  __  __  __
          / _ \ / __ \ / / / / \ \/ / / / / /
         / // // /_/ // /_/ /   \  / / /_/ /
        /____/ \____/ \____/    /_/  \____/
        """)

    for index, fl in enumerate(soup.find_all('li')):
        f_title = fl.find("a", target=True)
        f_time = fl.find("a", class_="head-ico4")
        fname = fl.find("a", class_="head-ico2")
        # f_room = fl.find("a", class_="head-ico3")
        print("\n----------- " + str(index) + " "
              + fname.get_text()
              + " ------------")
        if f_time:
            print(f_time.get_text(), f_title.get_text().encode("gb18030"))
        else:
            print(f_title.get_text().encode("gb18030"))


get_douyu_list(f_list_html)
