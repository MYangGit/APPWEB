const appConfig = {
  // 必填
  /** 设置app的名称 */
  appName: 'wireless',
  /** 显示在应用市场的名字 */
  displayName: "wireless",
  /** 设置app的启动命名 */
  startCommand: 'wireless',
  /** 设置app的启动标题 */
  startTitle: 'wireless',

  // 发布到MoHub的，必填
  /** 是否发布到MoHub */
  publishMoHub: false,
  /** 用户当前打开 MoHub 使用的端口 */
  MoHubPort: 47736, // 从用户地址栏获取syslabPort

  // 以下内容非必填，根据需要设置
  /** 设置app的图标 */
  icon: 'app-icon.png',
  /** 设置app的版本 */
  version: '0.0.0',
  /** 设置app的描述 */
  description: '这是一个无线应用demo',
  /** 设置app标题 中文 */
  appTitle: '无线应用demo',
  /** 设置app标题 英文 */
  appTitleEn: 'demo',
  /** 设置app的高度 */
  appHeight: 1057,
  /** 设置app的宽度 */
  appWidth: 850,
};

module.exports = {
 appConfig
}