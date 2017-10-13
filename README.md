# UPhys_Service
格物东南微信号后端服务

# 约定
* 数据库中除_id字段外其他字段若存储id，统一使用字符串

# 注意事项
* 从ORM获得的doc默认id为ObjectId，须转换后发送给前端
* ORM.old为废弃，将在后续版本中剔除