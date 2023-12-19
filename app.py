from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
# 从flask_wtf.file模块中导入FileField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms.fields import HiddenField
from flask import request
from markupsafe import Markup
import os

app = Flask(__name__, static_folder='static')  # 'static' 是静态资源文件夹的名称

app.config['STATIC_FOLDER'] = 'static'

# 为你的应用对象设置一个 secret key，使用 os.urandom(16) 来生成一个随机的 16 字节的字符串
app.secret_key = os.urandom(16)

# 配置 MySQL 数据库的参数
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '142857'
app.config['MYSQL_DB'] = 'fnav'

# 创建一个 MySQL 数据库连接对象
mysql = MySQL(app)

# 创建一个 SQLAlchemy 引擎对象，用于连接 MySQL 数据库
engine = create_engine('mysql://root:142857@localhost/fnav')
# 创建一个 SQLAlchemy 会话对象，用于管理数据库事务
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# 创建一个 SQLAlchemy 基类对象，用于定义模型
Base = declarative_base()
Base.query = db_session.query_property()


# 定义一个书签模型，继承自 SQLAlchemy 基类，对应于数据库中的 bookmarks 表
class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=False)
    box_shadow = Column(String(255), nullable=False)

    def __repr__(self):
        return '<Bookmark %r>' % self.name

# 创建一个书签模型视图的类，继承自 ModelView 类
class BookmarkModelView(ModelView):
    form_widget_args = {
        'icon': {'style': 'max-width: 450px;'}
    }
    
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


# 创建一个 Flask-Admin 对象，传入您的应用对象和一个标题参数
admin = Admin(app, name='后台管理系统')
# 使用 Flask-Admin 对象的 add_view 方法，添加您的书签模型视图，传入一个模型视图的实例，以及一个名称和分类参数
admin.add_view(BookmarkModelView(Bookmark, db_session, name='书签管理', category='数据管理'))


# 定义一个书签2模型，继承自 SQLAlchemy 的基类
class Bookmark2(Base):
    # 指定表名为 bookmarks2
    __tablename__ = 'bookmarks2'
    # 定义表中的字段，包括类型和主键
    category = Column(String(50), primary_key=True)
    name = Column(String(100), primary_key=True)
    link = Column(String(255))
    description = Column(String(255))



# 创建一个名为 '书签2管理' 的视图，用于管理 Bookmark2 模型，并指定要显示和编辑的所有属性
class Bookmark2ModelView(ModelView):
    column_list = ['category', 'name', 'link', 'description']  # 指定要在列表视图中显示的字段
    form_columns = ['category', 'name', 'link', 'description']  # 指定要在编辑/创建表单中显示的字段

admin.add_view(Bookmark2ModelView(Bookmark2, db_session, name='侧边栏书签管理', category='数据管理'))


@app.route('/')
def index():
    # 从数据库中查询所有的书签数据
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bookmarks')
    bookmarks = cur.fetchall()
    cur.close()
    # 将书签数据传递给模板，渲染页面
    return render_template('index.html', bookmarks=bookmarks)

@app.route('/get_bookmarks')
def get_bookmarks():
    # 从数据库中查询所有的书签数据
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bookmarks')
    bookmarks = cur.fetchall()
    cur.close()
    # 将书签数据转换为 JSON 格式，返回给前端
    bookmarks_list = []
    for bookmark in bookmarks:
        bookmarks_list.append({
            'name': bookmark[1],
            'link': bookmark[2],
            'icon': bookmark[3],
            'box_shadow': bookmark[4]
        })
    return jsonify(bookmarks_list)

# 定义一个路由，用于处理获取书签数据的请求
@app.route('/get_bookmarks2')
def get_bookmarks2():
    # 使用 SQLAlchemy 的 query 方法，查询所有的书签对象
    bookmarks = Bookmark2.query.all()
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



if __name__ == '__main__':
    # 在运行应用之前，创建所有的数据库表
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)


