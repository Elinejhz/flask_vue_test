# 导入 flask 和 flask_sqlalchemy
import yaml
from flask import Flask, request
from flask_restx import Resource, Api, Namespace
from flask_sqlalchemy import SQLAlchemy
# 实例化app 对象
from sqlalchemy import *
from flask_cors import *
from log_util import logger

# 创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
api = Api(app, version='1.0', title='Testcase API', description='A simple Testcase API')
CORS(app, supports_credentials=True)
# 用例的命名空间
case_ns = Namespace("case", description="用例管理")

with open("C:\softtest\pyenvs\python_testplatform_backend-master\\backend_flask\data.yml") as f:
    # result = yaml.safe_load(f)
    result = yaml.safe_load(f)
    username = result.get("database").get('username')
    password = result.get("database").get('password')
    server = result.get("database").get('server')
    db = result.get("database").get('db')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{username}:{password}@{server}/{db}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# SQLAlchemy 绑定 app
db = SQLAlchemy(app)


# 创建用例表
class TestCase(db.Model):
    # 表名
    __tablename__ = "testcase"
    # 用例ID 用例的唯 一标识
    id = db.Column(Integer, primary_key=True)
    # 用例的标题 或者文件名,限定 80个字符 ，不为空，并且唯一
    case_title = db.Column(String(80), nullable=False, unique=True)
    # 备注
    remark = db.Column(String(120))

db.create_all()

# @api.route("/testcase")
@case_ns.route("")
class TestCaseServer(Resource):
    get_paresr = api.parser()
    # 查询接口， 可以传id ，也可以不传id，
    # 不传id：就是返回 全部记录
    # 传id：返回查询到的对应的记录，如果未查到则返回 空列表
    get_paresr.add_argument("id", type=int, location="args")

    @case_ns.expect(get_paresr)
    def get(self):
        """
        测试用例的查找
        :return:
        """
        case_id = request.args.get("id")

        logger.info(f"type(request.args) <===== {type(request.args)}")
        logger.info(f"接收到的参数 <===== {case_id}")
        if case_id:
            # 如果不为空，查询操作
            case_data = TestCase.query.filter_by(id=case_id).first()
            logger.info(f"{case_data}")
            if case_data:
                datas = [{"id": case_data.id,
                          "case_title": case_data.case_title,
                          "remark": case_data.remark}]
                logger.info(f"要返回的数据为<======{datas}")
            else:
                datas = []
        else:
            # 为空，返回所有记录
            case_datas = TestCase.query.all()
            datas = [{"id": case_data.id,
                      "case_title": case_data.case_title,
                      "remark": case_data.remark} for case_data in case_datas]

        return datas

    post_paresr = api.parser()
    logger.info()
    post_paresr.add_argument("id", type=int, required=True, location="json")
    post_paresr.add_argument("case_title", type=str, required=True, location="json")
    post_paresr.add_argument("remark", type=str, location="json")

    @case_ns.expect(post_paresr)
    def post(self):
        """
        测试用例的新增
        :return:
        """
        # 获取请求数据
        case_data = request.json
        logger.info(f"接收到的参数<====== {case_data}")
        case_id = case_data.get("id")
        case_title = case_data.get("case_title")
        # 1) 若case_id为空，返回"ID不能为空"
        if case_id == '':
            return "ID cannot be empty."
        else:
            # 查询数据库，查看是否有记录
            exists_id = TestCase.query.filter_by(id=case_id).first()
            exists_titles = TestCase.query.filter_by(case_title=case_title).all()
            exists_id_latest = TestCase.query.order_by(TestCase.id.desc()).first()
            logger.info(f"根据id查询表结果为：{exists_id}")
            logger.info(f"查询表中最新一条数据的id为：{exists_id_latest.id}")
            # 2) 若根据id查询结果中case_title不为空，返回"case_title已存在"
            if exists_titles:
                return f"case_title {case_title} already exists in the table."
            # 2.1) 若根据id查询结果为空，则添加这条记录到库中
            # 2.2) 若id存在，不执行新增操作， 返回 40001错误码
            else:
                if not exists_id:
                    testcase = TestCase(**case_data)
                    logger.info(f"将要存储的内容为<======{testcase}")
                    db.session.add(testcase)
                    db.session.commit()
                    # 2.1.1) 若case_id为0，落库时，系统根据当前表中最新一条数据的id值+1 作为当前新增数据的id
                    if not case_id:
                        case_id = exists_id_latest.id +1
                        return {"code": 0, "msg": f"case id {case_id} success add."}
                    # 2.1.2) 若若case_id不为空，直接落库
                    else:
                        return {"code": 0, "msg": f"case id {case_id} success add."}
                else:
                    return {"code": 40001, "msg": f"case id {case_id} already exists in the table."}

    put_paresr = api.parser()
    put_paresr.add_argument("id", type=int, required=True, location="json")
    put_paresr.add_argument("case_title", type=str, required=True, location="json")
    put_paresr.add_argument("remark", type=str, location="json")

    @case_ns.expect(put_paresr)
    def put(self):
        """
        测试用例的修改
        :return:
        """
        case_data = request.json
        logger.info(f"接收到的参数<====== {case_data}")
        case_id = case_data.get("id")
        # 查询数据库，查看是否有记录
        exists = TestCase.query.filter_by(id=case_id).first()
        logger.info(f"查询表结果：{exists}")
        # 如果不存在，则 不执行修改操作 并返回 40002
        # 如果存在，执行修改操作
        if exists:
            case_data1 = {}
            case_data1["case_title"] = case_data.get("case_title")
            case_data1["remark"] = case_data.get("remark")
            TestCase.query.filter_by(id=case_id).update(case_data1)
            db.session.commit()
            return {"code": 0, "msg": f"case id {case_id} success change to {case_data1}"}
        else:
            return {"code": 40002, "msg": "case id {case_id} does not exist in the table."}

    delete_parser = api.parser()
    delete_parser.add_argument("id", type=int, location="json", required=True)

    @case_ns.expect(delete_parser)
    def delete(self):
        """
        测试用例的删除
        :return:
        """
        case_data = request.json
        case_id = case_data.get("id")
        logger.info(f"接收到的参数id <====={case_id}")
        exists = TestCase.query.filter_by(id=case_id).first()
        if exists:
            TestCase.query.filter_by(id=case_id).delete()
            db.session.commit()
            return {"code": 0, "msg": f"case id {case_id} success delete!"}
        else:
            return {"code": 40002, "msg": f"case id {case_id} does not exist in the table."}


api.add_namespace(case_ns, "/testcase")

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
