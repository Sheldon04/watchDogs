使用需要配置vant环境
（引用时也要注意引用的目录，引用在个文件的json文件中）
教程如下
步骤一：（需在miniprogram目录下）
# 通过 npm 安装
npm i @vant/weapp -S --production
步骤二：
将 app.json 中的 "style": "v2" 去除，小程序的新版基础组件强行加上了许多样式，难以覆盖，不关闭将造成部分组件样式混乱。
步骤三：
修改 project.config.json
需要手动在 project.config.json 内添加如下配置，使开发者工具可以正确索引到 npm 依赖的位置。
{
  ...
  "setting": {
    ...
    "packNpmManually": true,
    "packNpmRelationList": [
      {
        "packageJsonPath": "./package.json",
        "miniprogramNpmDistDir": "./miniprogram/"
      }
    ]
  }
}
步骤四：构建npm包。
![image](https://user-images.githubusercontent.com/67893995/126578390-75576566-3693-49f7-afd4-724fdeca1ac9.png)
