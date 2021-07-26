
const cloud = require('wx-server-sdk')
cloud.init()
//引入发送邮件的类库
var nodemailer = require('nodemailer')
// 创建一个SMTP客户端配置
var config = {
  host: 'smtp.qq.com', //网易163邮箱 smtp.163.com
  port: 465, //网易邮箱端口 25
  auth: {
    user: '1241110779@qq.com', //邮箱账号
    pass: 'qpzqnsxjqqjsfgdb' //邮箱的授权码
  }
};
// 创建一个SMTP客户端对象
var transporter = nodemailer.createTransport(config);
// 云函数入口函数
exports.main = async(event, context) => {
  // 创建一个邮件对象
  var mail = {
    // 发件人
    from: '管理员 <1241110779@qq.com>',
    // 主题
    subject: '验证码',
    // 收件人
    to: '1241110779@qq.com',
    // 邮件内容，text或者html格式
    text: "验证码为："+"1", //可以是链接，也可以是验证码
  };


  let res = await transporter.sendMail(mail);
  return res;




}
