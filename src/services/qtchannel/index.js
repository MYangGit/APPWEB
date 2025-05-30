
import defer from 'defer-promise'

let qtWebInitPromise = null;

const ensureBackendReady = async () => {
  if (window.backendApi) return window.backendApi;
  if (!qtWebInitPromise) {
    qtWebInitPromise = new Promise((resolve, reject) => {
      try {
        if(typeof qt === 'undefined') {
            resolve(false)
            return;
        };
        new QWebChannel(qt.webChannelTransport, channel => {
          const backend = channel.objects.backend;
          window.backendApi = backend;
          // 监听后端内容变化
          backend.contentChanged.connect(handleResponse);
          resolve(backend);
        });
      } catch (err) {
        reject(err);
      }
    });
  }
  return qtWebInitPromise;
};

let deferred = defer();
export const postQt = async (config) => {
  console.warn('postQt called with config:', JSON.stringify(config));
  const backend = await ensureBackendReady();
  if (!backend) {
    return {
      type: 'error',
      message: 'Backend not ready or QWebChannel not initialized.'
    };
  }
  backend.jscall(JSON.stringify(config));
  deferred  = defer();
  let res;
  try {
    res = await deferred.promise
  } catch (error) {
    res = {
      type: 'error',
      message: error
    }
  }
  return res
};

// 监听到的后端内容变化
const handleResponse = (response) => {
  console.warn('Received response:', response);
  try {
     response = JSON.parse(response);
    if (response.code >= 400) {
      deferred.reject(new ApiError(response.code, response.msg));
    } else {
      deferred.resolve(response);
    }
  } catch (err) {
    console.error('Response processing error:', err);
    deferred.reject(err);
  } 
};

