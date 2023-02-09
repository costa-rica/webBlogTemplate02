import os
from bs4 import BeautifulSoup

def templates_file_path_and_name(filename, root_path):
    temp_file_name = "temporary_file_for_path_name.txt"
    f = open(temp_file_name,'w')
    f.write(root_path)
    f.write(os.path.join('/templates/blogposts', filename))
    f.close()

    f = open(temp_file_name,'r')
    file_path_and_name = f.readlines()[0]
    f.close()
    return file_path_and_name


def templates_file_path(root_path):
    temp_file_name = "temporary_file_for_path.txt"
    f = open(temp_file_name,'w')
    f.write(root_path)
    f.write('/templates/blogposts')
    f.close()

    f = open(temp_file_name,'r')
    file_path = f.readlines()[0]
    f.close()
    return file_path


def create_new_html_text(html_file_path_and_name, formDict):
    #read html into beautifulsoup
    with open(html_file_path_and_name) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #Get title and replace
    if formDict.get('title'):
        soup.p.find('span').contents[0].replaceWith(formDict.get('title'))
        title = formDict.get('title')
    else:
        title = soup.p.find('span').contents[0]


    #get all images
    image_list = soup.find_all('img')
    # check all images have src or remove
    for img in image_list:
        try:
            if img.get('src') == "":
                image_list.remove(img)
        except AttributeError:
            image_list.remove(img)

    #loop thorugh image
    static_folder_blogpost_path = os.path.join("../static/images/blogpost_images/")
    for img in image_list:
        img['src']=f"{static_folder_blogpost_path}{img['src']}"

    return (title, str(soup))