import cryptoJs from 'crypto-js';
import { cloneDeep } from 'lodash';

export function deepCopy(target) {
  return cloneDeep(target);
}

export function swap(arr, i, j) {
  const temp = arr[i];
  arr[i] = arr[j]
  arr[j] = temp;
}

export function $(selector) {
  return document.querySelector(selector);
}

const components = ['VText', 'RectShape', 'CircleShape'];
export function isPreventDrop(component) {
  return !components.includes(component) && !component.startsWith('SVG');
}

export function encryptDes(message, key) {
  let keyHex = cryptoJs.enc.Utf8.parse(key);
  let option = { mode: cryptoJs.mode.ECB, padding: cryptoJs.pad.Pkcs7 };
  let encrypted = cryptoJs.DES.encrypt(message, keyHex, option);
  return encrypted.toString();
}

export function generateSalt(length) {
  let char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let chars = '';
  for (let i = 0; i < length; i++) {
    chars += char.charAt(parseInt(Math.random() * char.length));
  }
  return chars;
}

export function generatePassword(rawPassword) {
  let salt = generateSalt(8);
  let base64Salt = Buffer.from(salt, 'utf-8').toString('base64');

  let desPassword = encryptDes(rawPassword, base64Salt.substring(0, 8));
  return Buffer.from(desPassword + salt, 'utf-8').toString('base64');
}

/**
 * reg
 * @des 正则(手机号/邮箱)
 *
 */
export function reg(type, value) {
  let reg;
  switch (type) {
    case 'phone':
      reg = /^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/g;
      break;
    case 'mail':
      reg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/g;
      break;
    case 'positiveInteger':
      reg = /[\d]/;
  }
  return reg.test(value);
}

/**
 * 生成唯一id
 * @param {String} evt
 *
 */
export function createUuid() {
  let s = [];
  let hexDigits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  for (let i = 0; i < 36; i++) {
    s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
  }
  s[14] = '4';
  // eslint-disable-next-line no-bitwise
  s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);
  // eslint-disable-next-line no-multi-assign
  s[8] = s[13] = s[18] = s[23] = '-';
  let uuid = s.join('');
  return uuid;
}

// 导出文件
export function exportJson(name, data) {
  let blob = new Blob([data]); //  创建 blob 对象
  let link = document.createElement('a');
  link.href = URL.createObjectURL(blob); //  创建一个 URL 对象并传给 a 的 href
  link.download = name; //  设置下载的默认文件名
  link.click();
}

export function getQueryVariable(variable) {
  const query = window.location.hash.split('?')[1];
  const vars = query ? query.split('&') : [];
  for (let i = 0; i < vars.length; i++) {
    const pair = vars[i].split('=');
    if (pair[0] === variable) {
      return pair[1];
    }
  }
  return false;
}

export const fileToBase64 = file => {
  let reader = new FileReader();
  reader.readAsDataURL(file);
  return new Promise((resolve, reject) => {
    reader.onload = function (e) {
      resolve(e.target.result);
    };
  })
};

export function getValueByDotKey(obj, dotKey) {
  const keys = dotKey.split('.');
  let value = obj;
  for (let key of keys) {
    if (value.hasOwnProperty(key)) {
      value = value[key];
    } else {
      return undefined; // 如果键不存在，返回 undefined
    }
  }
  return value;
}

function setValueByDotKey(obj, dotKey, value) {
  const keys = dotKey.split('.');
  const lastKey = keys.pop();
  let currentObj = obj;
  for (let key of keys) {
    if (!currentObj.hasOwnProperty(key) || typeof currentObj[key] !== 'object') {
      currentObj[key] = {};
    }
    currentObj = currentObj[key];
  }
  currentObj[lastKey] = value;
}

export const getComputedGet = (key, dataBinds, stateSet, propValue) => {
  let keys = dataBinds[key]
  if (keys) {
    let data = getValueByDotKey(stateSet, keys.join('.'))
    return data
  } else {
    return propValue[key];
  }
};

export const getComputedSet = (key, dataBinds, stateSet, propValue, val) => {
  let keys = dataBinds[key]
  if (keys) {
    setValueByDotKey(stateSet, keys.join('.'), val)
  } else {
    propValue[key] = val;
  }
};

/**
 * @description: 判断一个东西是不是空 空格 空字符串 undefined 长度为0的数组及对象会被认为是空的
 * @param key
 * @returns {boolean}
 */
export const isEmpty = (key) => {
  switch (typeof key) {
    case 'string':
      return key.trim().length === 0;
    case 'object':
      return key === null || key === undefined || Object.keys(key).length === 0;
    case 'boolean':
      return false;
    case 'number':
      return Number.isNaN(key);
    default:
      return true;
  }
};

/**
 * @description: 命名判重
 * @param {string} name
 * @param {arr} list
 * @returns string
 */
export const nameRepeat = (name, list) => {
  let newName = name;
  let ext = 1;
  while (list.some(item => item.name === newName)) {
    newName = `${name}_${ext}`;
    ext++;
  }
  return newName;
}