self.importScripts('spark-md5.min.js');

var BLOCK_SIZE = 4 * 1024 * 1024;

onmessage = function (message) {
    var obj = message.data;
    var blockCount = Math.ceil(obj.data.size / BLOCK_SIZE);
    console.log('for worker' + obj.wid + ' will send ' + blockCount + ' blocks');

    for (var i = 0; i < blockCount; ++i) {
        var name = obj.name;
        var seq = i + obj.seq;
        var data = obj.data.slice(i * BLOCK_SIZE, (i + 1) * BLOCK_SIZE);
        send(data, name, seq);
    }


    function send(data, name, seq) {

        var fileReader = new FileReader();
        fileReader.readAsBinaryString(data);
        fileReader.onloadend = function () {

            var formData = new FormData();
            formData.append('md5', md5(fileReader.result));
            formData.append('seq', seq);
            formData.append('name', name);
            formData.append('data', data);

            console.log('send: ' + name + ' seq: ' + seq + '\tmd5: ' + md5(fileReader.result));
            _send(formData);
        };
    }

    function _send(formData) {
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

    function md5(binaryString) {
        return new SparkMD5().appendBinary(binaryString).end();
    }

};