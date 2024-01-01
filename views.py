# views.py

from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from markupsafe import Markup
from flask_admin.menu import MenuLink
from models import Bookmark, Bookmark2  # 导入模型定义
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:142857@localhost/fnav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###########################################################################################################################
# 创建一个书签模型视图的类，继承自 ModelView 类
class BookmarkModelView(ModelView):
    # 在这里，您可以定义一些自定义的属性和方法，例如表单字段，列过滤器，验证规则等
    # 例如，为 icon 字段添加一个 FileField 类型的表单字段，用于上传图片文件
    form_extra_fields = {
        'icon': FileField('Icon')
    }

    column_formatters = {   
        'icon': lambda v, c, m, p: Markup(f'<img src="{m.icon}" style="max-width:100px;max-height:100px;">'),
        'box_shadow': lambda v, c, m, p: Markup(f'<div style="width: 50px; height: 50px; border: 1px solid #ccc; background-color: white; box-shadow: 0px 0px 5px {m.box_shadow};"></div>')
    }

    # 在添加新书签时触发的方法
    def on_model_change(self, form, model, is_created):
        icon_file_data = request.files.get(form.icon.name)
        if icon_file_data:
            icon_filename = secure_filename(icon_file_data.filename)
            icon_file_path = os.path.join(app.config['STATIC_FOLDER'], 'img', icon_filename)
            icon_file_data.save(icon_file_path)
            model.icon = '/static/img/' + icon_filename  # 设置完整的图片路径

# 创建一个名为 '书签2管理' 的视图，用于管理 Bookmark2 模型，并指定要显示和编辑的所有属性
class Bookmark2ModelView(ModelView):
    column_list = ['category', 'name', 'link', 'description']  # 指定要在列表视图中显示的字段
    form_columns = ['category', 'name', 'link', 'description']  # 指定要在编辑/创建表单中显示的字段

admin = Admin(app, name='后台管理系统')
admin.add_view(BookmarkModelView(Bookmark, db.session, name='首页书签管理'))
admin.add_view(Bookmark2ModelView(Bookmark2, db.session , name='侧边栏书签管理'))

# 添加自定义导航链接
admin.add_link(MenuLink(name='回导航页', url='/'))


###########################################################################################################################
def get_bookmarks_from_db():
    # 使用 SQLAlchemy 的 db.session 查询获取所有书签
    bookmarks = db.session.query(Bookmark).all()
    return bookmarks

###########################################################################################################################

@app.route('/')
def index():
    bookmarks = get_bookmarks_from_db()
    return render_template('index.html', bookmarks=bookmarks)

@app.route('/get_bookmarks') 
def get_bookmarks():
    bookmarks = get_bookmarks_from_db()
    bookmarks_list = []
    for bookmark in bookmarks:
        bookmarks_list.append({
            'name': bookmark.name,  # 修改这里
            'link': bookmark.link,  # 修改这里
            'icon': bookmark.icon,  # 修改这里
            'box_shadow': bookmark.box_shadow  # 修改这里
        })
    return jsonify(bookmarks_list)


# 定义一个路由，用于处理获取书签数据的请求
@app.route('/get_bookmarks2')
def get_bookmarks2():
    # 使用 db.session 对象查询 Bookmark2 数据
    bookmarks = db.session.query(Bookmark2).all()
    # 定义一个空列表，用于存储书签数据
    data = []
    # 遍历每个书签对象，将其转换为字典，并添加到列表中
    for bookmark in bookmarks:
        data.append({
            'category': bookmark.category,
            'name': bookmark.name,
            'link': bookmark.link,
            'description': bookmark.description
        })
    # 使用 jsonify 函数，将列表转换为 JSON 格式，并返回响应
    return jsonify(data)

###########################################################################################################################

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)