import sampling
import time
import json
import os
from flask import Flask, make_response, render_template, request, send_file
from flask_restful import Resource, Api,reqparse

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)
check = [0]

class sampling_data(Resource):
    def get(self):
        while(1):
            if check[0]==1:
                check[0]=0
                res = make_response(json.dumps({'version':sampling.version},ensure_ascii=False))
                res.headers['Content-type'] = 'application/json'
                print("send call")
                return res
            else:
                pass

    def post(self):
        json_data=request.get_json()

        index=json_data["index"]
        carrier_frequency=json_data["carrier_frequency"]
        amplitude=json_data["amplitude"]
        phase=json_data["phase"]
        sampling.sampling_rate=json_data["sampling_rate"]

        sampling.do_sampling(index,carrier_frequency,amplitude,phase)
        while(1):
            if os.path.isfile(basedir+"/templates/figures/result"+str(sampling.version)+".svg"):
                check[0]=1
                print("make image")
                break
            else:
                pass

class view_html(Resource):
    def get(self):
        res = make_response(render_template('view_sampling.html'))
        res.headers['Content-type'] = 'text/html'
        return res

class return_js(Resource):
    def get(self,directory):
        res = make_response(render_template("js/"+directory))
        res.headers['Content-type'] = 'text/javascript'
        return res

class return_img(Resource):
    def get(self,directory):
        res = make_response(render_template("figures/" + directory))
        res.headers['Content-type'] = 'image/svg+xml'
        os.remove(basedir + "/templates/figures/result"+str(sampling.version)+".svg")
        sampling.version+=1
        print("remove img")
        return res


api.add_resource(sampling_data, '/send')
api.add_resource(view_html, '/sample')
api.add_resource(return_js,'/js/<string:directory>')
api.add_resource(return_img,'/figures/<string:directory>')

if __name__ == '__main__':
    # app.run(debug=True)        # 디버그 모드 실행
    app.run(host='0.0.0.0')     # 외부에서 접속가능한 서버로 실행
