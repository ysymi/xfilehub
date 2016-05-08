var BLOCK_SIZE = 4 * 1024 * 1024;
    
onmessage = function (message) {
    var obj = message.data;
    var blockCount = Math.ceil(obj.data.size / BLOCK_SIZE);
    console.log('for this worker : ' + obj.data.size + ' / ' + BLOCK_SIZE + ' = ' + blockCount);

    for (var i = 0; i < blockCount; ++i) {
        var formData = new FormData();
        formData.append('data', obj.data.slice(i * BLOCK_SIZE, (i + 1) * BLOCK_SIZE));
        formData.append('name', obj.name);
        formData.append('seq', i + obj.seq);

        upload(formData);
    }
};


function upload(formData) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        var DONE = 4;
        var OK = 200;
        if (xhr.readyState === DONE) {
            if (xhr.status === OK) {
                postMessage('success');
            } else {
                postMessage('failure');
            }
        }
    };

    xhr.open('POST', '/upload', true);
    xhr.send(formData);
}