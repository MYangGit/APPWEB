export const parseJuliaFn = (code) => {
    return  `async ({dataCenter, globalUtils}, eventParams) => {
          const { post, getFilePath, handleJuliaCode } = globalUtils
          let juliaCode = \`${code}\`
          let code = handleJuliaCode(juliaCode, dataCenter, "gd", getFilePath())
          function assignValues(obj, obj2) {
             for (let key in obj) {
                if (obj2.hasOwnProperty(key)) {
                   obj2[key] = obj[key];
                }
             }
          }
          console.log('excuteCode', code)
          let res = await post({
             key: 'excuteCode',
             command: 'excute',
             code
          })
          console.log('res', res.data.value)
          if (res.data && res.data.value) {
             assignValues(res.data.value, dataCenter)
          }
       }
    `;
 }