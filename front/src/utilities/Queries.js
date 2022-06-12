function getCookieByName(name) {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match?.[2];
}

function deleteCookie(name) {
  if (getCookieByName(name)) {
    document.cookie = `${name}=`
        // ((path) ? ";path="+path:"")+
        // ((domain)?";domain="+domain:"") +
        + ';expires=Thu, 01 Jan 1970 00:00:01 GMT';
  }
}

const fetchGet = async (url) => fetch(url, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    username: getCookieByName('username'),
  },
});

const fetchPostJson = async (url, json) => fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    username: getCookieByName('username'),
    project: getCookieByName('project'),
  },
  body: json,
});

export {
  fetchGet, fetchPostJson, getCookieByName, deleteCookie,
};

export default fetchPostJson;
