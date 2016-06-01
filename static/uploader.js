self.importScripts('spark-md5.min.js');

var BLOCK_SIZE = 4 * 1024 * 1024;

onmessage = function (message) {
    var obj = message.data;
    var blockCount = Math.ceil(obj.data.size / BLOCK_SIZE);
    console.log('worker' + obj.wid + ' will send ' + blockCount + ' blocks');

    for (var i = 0; i < blockCount; ++i) {
        var name = obj.name;
        var tot = obj.tot;
        var seq = i + obj.seq;
        var data = obj.data.slice(i * BLOCK_SIZE, (i + 1) * BLOCK_SIZE);
        console.log('worker' + obj.wid + ' will send ' + seq);
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

        // var last = 0;
        // xhr.upload.onprogress = function (event) {
        //     if (event.lengthComputable) {
        //         var sent = event.loaded - last;
        //
        //         postMessage('sent:' + sent);
        //         postMessage(sent);
        //
        //     }
        // };

        var startTime = new Date().getTime();
        xhr.open('POST', '/chunks', true);
        xhr.send(formData);
        xhr.onload = function () {
            var endTime = new Date().getTime();
            console.log('sent chunk' + formData.get('seq') + ' use ' + (endTime - startTime) + 'ms');
            postMessage('success');
        };
    }

    function md5Sum(binaryString) {
        return new SparkMD5().appendBinary(binaryString).end();
    }

};