from flask import Flask, render_template, request, jsonify, make_response, current_app, \
    flash, redirect, url_for
import os
import json
from config import config
from models import sess, Blogposts
from werkzeug.utils import secure_filename
import zipfile

from utils import templates_file_path_and_name, templates_file_path, create_new_html_text
from bs4 import BeautifulSoup
import shutil

app = Flask(__name__)
app.config.from_object(config)


@app.route("/", methods=["GET","POST"])
def home():

    posts_list = [{"id":1,"title":"Oblix"}]

    posts = sess.query(Blogposts).all()
    if len(posts) > 0:
        posts_list = [{"id":post.id,"title":post.title,"doc_name":post.word_doc_name} for post in posts]

    if request.method == "POST":
        formDict = request.form.to_dict()

        if formDict.get('delete'):
            post_id = formDict.get('delete')
            post_for_delete = sess.query(Blogposts).filter_by(id = post_id).first()

            # remove word doc from _database directiory
            os.remove(templates_file_path_and_name(post_for_delete.word_doc_name, app.config.root_path))

            shutil.rmtree(os.path.join("static/images/blogpost_images/", post_for_delete.images_folder_name))
            
            # remove from database
            sess.query(Blogposts).filter_by(id = post_id).delete()
            sess.commit()

            flash('Deleting a file - attention -', 'warning')
            return redirect(request.url)

        elif formDict.get('view'):
            post_id = formDict.get('view')
            return redirect(url_for('view_post', id = post_id))

        ###############################
        # Uploading Blogpost Word doc #
        ###############################
        else:
            file = request.files.get('word_doc_upload')
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No file selected.', 'warning')
                return redirect(request.url)
            elif file:
                filename = secure_filename(file.filename)

                # check if file name already uploaded:
                existing_file_names_list = [i.name for i in os.scandir(templates_file_path(app.root_path))]
                if filename in existing_file_names_list:
                    flash('A flie with the same name has already been saved. Change file name and try again.', 'warning')
                    return redirect(request.url)

                # Accept folder images
                if request.files.get('folder_images').filename != "":
                    print('- folder_images accessed --------')
                    zip_folder_object = request.files['folder_images']

                    zip_folder_name = zip_folder_object.filename
                    
                    path_to_zip_file = os.path.join(current_app.static_folder,'images','blogpost_images',secure_filename(zip_folder_name))
                    zip_folder_object.save(path_to_zip_file)

                    #unzip
                    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                        print("- unzipping file --")
                        unzipped_images_foldername = zip_ref.namelist()[0]
                        zip_ref.extractall(os.path.join(current_app.static_folder,'images','blogpost_images'))

                    # delete compressed file
                    os.remove(path_to_zip_file)

                # Save html to templates path 
                html_file_path_and_name = templates_file_path_and_name(filename, app.config.root_path)
                file.save(html_file_path_and_name)

                # read uploaded html and replace image and title refrences if needed
                title, new_html_text = create_new_html_text(html_file_path_and_name, formDict)

                # Save new soup html
                with open(html_file_path_and_name,"w") as new_file:
                    new_file.write(new_html_text)

                new_post = Blogposts(
                    title=title,
                    word_doc_name=filename,
                    images_folder_name = unzipped_images_foldername
                    )
                sess.add(new_post)
                sess.commit()

                flash('File successfully uploaded!', 'success')
                return redirect(url_for('home', name=filename))

    return render_template("home.html", posts_list=posts_list)


@app.route("/view_post/<id>", methods=["GET","POST"])
def view_post(id):

    post = sess.query(Blogposts).filter_by(id= id).first()

    blog_file_path="/blogposts/" + post.word_doc_name


    print("- blog_file_path -")
    print(blog_file_path)


    return render_template("view_post.html", blog_title = post.title, blog_file_path=blog_file_path, render_template=render_template)


if __name__ == '__main__':
    app.run()