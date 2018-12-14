function createNode(element) {
    return document.createElement(element);
}

function append(parent, el) {
  return parent.appendChild(el);
}

const url = '/posts/wangyang';
fetch('/posts/wangyang')
    .then(response => response.json())
    .then(receive => {
        var test = receive.data;
        console.log(test)
         $("#id_username").text(test[0].content)
    })
    .catch(error => console.error(error))