# PyUnityboxDemo
--------------------------------------
#概述
该工程只是为了对UnityBox的API接口做简单的示范，对于界面的样式、代码风格、实现方式都请勿模仿。
#环境搭建
```bash
#如果为安装pip请自行搜索如何安装
#如果已经安装了virtualenv和virtualenvwrapper请忽略这两玩意的安装
pip install virtualenv
pip install virtualenvwrapper
vim ~/.bash_profile
#添加 source /usr/local/bin/virtualenvwrapper.sh

#创建虚拟环境
mkvirtualenv PyUnityBoxDemoEnv
#以下为DEMO的依赖，紧紧依赖flask和requests
pip install flask
pip install requests

#进入DEMO的主目录
cd PyUnityboxDemo
#初始化数据库
sqlite3 /tmp/demo.db < schema.sql
```

#API接入修改
修改demo.py文件中的如下代码,修改后记得删除抛出的异常段。如果不清楚如何申请获得账号，可以参考[Unity-Box Account](https://api.unity-box.com/services/doc/en#account)
```python demo.py
SECRET_KEY = 'development key'
#INPUT YOUR API USER,PASSWORD AND CLIENT_ID , THEN DELETE THE LINE.
raise Exception,'PLEASE INPUT YOUR API USER,PASSWORD AND CLIENT_ID'
#TODO 
API_USERNAME = 'PLEASE_INPUT_YOUR_API_USER'
#TODO 
API_PASSWORD = 'PLEASE_INPUT_YOUR_API_PASSWORD'
#TODO 
API_CLIENT_ID = 'PLEASE_INPUT_YOUR_API_CLIENT_ID'
```

#运行工程
```bash
python demo.py
```

#API相关DEMO代码
为了保证token的安全，建议建议需要token验证的操作都放在后台发起请求。
##登录
```python 
    params = {'client_id': app.config['API_CLIENT_ID'],\
              'grant_type': 'password',\
              'password':app.config['API_PASSWORD'],\
              'username':app.config['API_USERNAME']
              }

    r = requests.post("https://api.unity-box.com/oauth2/access_token",\
                      data=params,verify=False)
    if r.status_code == 200:
        responseDict =  r.json()
        app.config['ACCESS_TOKEN'] = responseDict['access_token']
        app.config['TOKEN_TYPE'] = responseDict['token_type']
        app.config['EXPIRES'] = responseDict['expires_in']
        app.config['TOKEN_SCOPE'] = responseDict['scope']
```

##获取自提点
```javascript
$.ajax({
  async:true,
  cache:true,
  url:"https://api.unity-box.com/services/pickuppoints/",
  success:function(data,status){
    if(status!=="success"||!data){
      return;
    }
    var pickuppoints = data.results;
    var select = $("#select_pickuppoint").find("select");
    select.empty();
    $("<option value=''>Please select a pickup point</option>").appendTo(select);
    for(var index=0;index<pickuppoints.length;index++){
      var point = pickuppoints[index];
      $("<option value='"+point.id+"'>"+point.name+"</option>").appendTo(select);
    }
  },
  error:function(){
    console.log(arguments);
  }
});
```

##提交订单
```python
order_dict = {'product_name':product_name,'consignee_name':consignee_name,'otp_phone_number':otp_phone_number,'consignee_email':consignee_email,'pickuppoint':pickuppoint}
headers = {'content-type': 'application/json','Authorization':'%s %s' % (app.config['TOKEN_TYPE'],app.config['ACCESS_TOKEN'])}
r = requests.post('https://api.unity-box.com/services/order/', data=json.dumps(order_dict), headers=headers,verify=False)
print r.json()
```

##获取qrcode
```javascript
    function print_qrcode(serial_number){
       var printWindow = window.open('', 'Print Window','height=500,width=600');

       printWindow.document.write('<html><head><title>Print Window</title>');

       printWindow.document.write('<style type="text/css" media="print">        @page         {            size: auto;   /* auto is the current printer page size */            margin: 0mm;  /* this affects the margin in the printer settings */        }        body         {            background-color:#FFFFFF; border: solid 0px black ; margin: 0px; /* the margin on the content before printing */       } ');

       printWindow.document.write(' @media screen and (-webkit-min-device-pixel-ratio:0) { .webkit { font-size:9px; -webkit-transform: scale(0.75) translate(-3px, 0px); letter-spacing: 1px;  } } ');

       printWindow.document.write('</style>' );
       printWindow.document.write('</head><body style="margin:0px 0px 0px 0px" onload="window.print();"');

       printWindow.document.write('<div style="position: absolute; left:4px; height:200px; width:144px; top:4px; font-family:Arial,Gadget,sans-serif;"></div>');

       printWindow.document.write('<div style="position: absolute; left:4px; height:200px; width:300px; top:4px; font-family:Arial,Gadget,sans-serif;">');
       printWindow.document.write('  <div style="position:relative; left:0px; top:0px;"><p style="text-align:center; margin-top:0px; margin-bottom:0px; padding:0px;"><img src="https://api.unity-box.com/services/qrcodedetail/'+serial_number+'.png" style=" width:300px; height:200px; margin:0px 0px 0px 0px; " /></p></div>' );
       printWindow.document.write('</div>' );

       printWindow.document.write('</body></html> ');
       printWindow.document.close();
    }
```

##获取订单状态
```js
    function trace_order(serial_number){
      var box = UnityBox.box({selector:"#trace"});
      box.trace_parcel(serial_number);
    }
```

```html
...
<body>
...
  <div style="width:600px;margin:auto;height:500px;" id="trace">
  </div>
...
</body>
```