self.importScripts('spark-md5.min.js');

var BLOCK_SIZE = 4 * 1024 * 1024;

onmessage = function (message) {
    var obj = message.data;
    var blockCount = Math.ceil(obj.data.size / BLOCK_SIZE);
    console.log('for worker' + obj.wid + ' will send ' + blockCount + ' blocks');

    for (var i = 0; i < blockCount; ++i) {
        var name = obj.name;
        var tot = obj.tot;
        var seq = i + obj.seq;
        var data = obj.data.slice(i * BLOCK_SIZE, (i + 1) * BLOCK_SIZE);
        send(data, name, seq, tot);
    }


    function send(data, name, seq, tot) {

        var fileReader = new FileReader();
        fileReader.readAsBinaryString(data);
        fileReader.onloadend = function () {

            var md5 = md5Sum(fileReader.result);
            var formData = new FormData();
            formData.append('md5', md5);
            formData.append('tot', tot);
            formData.append('seq', seq);
            formData.append('name', name);
            formData.append('data', data);

            console.log('send: ' + name + ' seq: ' + seq + '\tmd5: ' + md5);
            ajaxSend(formData);
        };
    }

    function ajaxSend(formData) {
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
        xhr.open('POST', '/chunks', true);
        xhr.send(formData);
    }

    function md5Sum(binaryString) {
        return new SparkMD5().appendBinary(binaryString).end();
    }

};