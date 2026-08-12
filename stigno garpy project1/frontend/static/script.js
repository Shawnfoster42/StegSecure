// ================= TAB SWITCHING =================
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.style.display = 'none');

        btn.classList.add('active');
        document.getElementById(btn.dataset.target).style.display = 'block';
    });
});

// ================= FILELIST HELPER =================
function createFileList(file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    return dt.files;
}

// ================= PREVIEW =================
function updatePreview(file, preview, type) {
    if (!file) {
        preview.innerHTML = '';
        return;
    }

    if (type === 'image') {
        preview.innerHTML = `<img src="${URL.createObjectURL(file)}" width="200">`;
    } 
    else if (type === 'audio') {
        preview.src = URL.createObjectURL(file);
        preview.load();
    } 
    else if (type === 'video') {
        preview.innerHTML = `<p>Selected file: ${file.name}</p>`;
    }
}

// ================= FILE VALIDATION =================
function handleFile(file, type, input, preview) {
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();

    if (type === 'audio' && ext !== 'wav') {
        alert("Only WAV audio supported");
        input.value = '';
        return;
    }

    if (type === 'video' && !['avi', 'mp4', 'mov'].includes(ext)) {
        alert("Only AVI / MP4 / MOV supported");
        input.value = '';
        return;
    }

    input.files = createFileList(file);
    updatePreview(file, preview, type);
}

// ================= DROP AREA =================
function setupDropArea(dropId, inputId, previewId, type) {
    const drop = document.getElementById(dropId);
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    drop.addEventListener('dragover', e => {
        e.preventDefault();
        drop.classList.add('dragover');
    });

    drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));

    drop.addEventListener('drop', e => {
        e.preventDefault();
        drop.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0], type, input, preview);
    });

    input.addEventListener('change', () => {
        handleFile(input.files[0], type, input, preview);
    });
}

setupDropArea('imageDrop', 'imageFile', 'imagePreview', 'image');
setupDropArea('audioDrop', 'audioFile', 'audioPreview', 'audio');
setupDropArea('videoDrop', 'videoFile', 'videoPreview', 'video');

// ================= MAIN SEND FUNCTION =================
function sendFile(endpoint, fileId, msgId, passId, resultId, action) {

    const fileInput = document.getElementById(fileId);
    const messageInput = document.getElementById(msgId);
    const passwordInput = document.getElementById(passId);
    const resultEl = document.getElementById(resultId);
    const progressBar = document.getElementById('progressBar');

    const file = fileInput.files[0];
    if (!file) {
        alert("Select a file first");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    if (action === 'encode' && messageInput) {
        formData.append('message', messageInput.value);
    }

    if (passwordInput && passwordInput.value) {
        formData.append('password', passwordInput.value);
    }

    progressBar.style.width = '0%';
    resultEl.innerText = "Processing...";

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            progressBar.style.width = (e.loaded / e.total) * 100 + '%';
        }
    };

    xhr.onload = () => {

        // ================= VIDEO ENCODE / DECODE =================
        if (fileId === 'videoFile') {
            if (xhr.status === 200) {
                try {
                    const data = JSON.parse(xhr.responseText);

                    if (action === 'encode') {
                        // Show auto-generated password
                        if (data.password) {
                            document.getElementById('videoPasswordResult').value = data.password;
                        }
                        // Download encrypted video
                        const a = document.createElement('a');
                        a.href = data.file_url;
                        a.download = "enc_" + file.name;
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                        resultEl.innerText = "Video encrypted successfully!";
                    }

                    if (action === 'decode') {
                        if (data.file_url) {
                            const a = document.createElement('a');
                            a.href = data.file_url;
                            a.download = "dec_" + file.name;
                            document.body.appendChild(a);
                            a.click();
                            a.remove();
                            resultEl.innerText = "Video decrypted successfully!";
                        } else {
                            resultEl.innerText = "Error: " + data.error;
                        }
                    }

                } catch (err) {
                    resultEl.innerText = "Invalid server response";
                }
            } else {
                resultEl.innerText = "Video processing failed: " + xhr.statusText;
            }
            return;
        }

        // ---------- DECODE (IMAGE / AUDIO) ----------
        if (action === 'decode') {
            try {
                const data = JSON.parse(xhr.responseText);
                resultEl.innerText = data.message 
                    ? "Decoded Message: " + data.message 
                    : "Error: " + data.error;
            } catch {
                resultEl.innerText = "Decode failed";
            }
            return;
        }

        // ---------- ENCODE (IMAGE / AUDIO) ----------
        if (xhr.status === 200) {
            const blob = new Blob([xhr.response]);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "enc_" + file.name;
            document.body.appendChild(a);
            a.click();
            a.remove();
            resultEl.innerText = "Encoding complete!";
        }
    };

    // Video endpoint override
    const finalEndpoint =
        fileId === 'videoFile'
            ? action === 'encode'
                ? '/video/encode'
                : '/video/decode'
            : endpoint;

    xhr.open('POST', finalEndpoint);
    xhr.responseType = fileId === 'videoFile' ? 'text' : (action === 'encode' ? 'blob' : 'text');
    xhr.send(formData);
}

// ================= BUTTONS =================
['image', 'audio', 'video'].forEach(type => {
    document.getElementById(`${type}EncodeBtn`).onclick = () =>
        sendFile('/encode', `${type}File`, `${type}Message`, `${type}Password`, `${type}Result`, 'encode');

    document.getElementById(`${type}DecodeBtn`).onclick = () =>
        sendFile('/decode', `${type}File`, `${type}Message`, `${type}Password`, `${type}Result`, 'decode');
});

// ================= PASSWORD TOGGLE =================
const toggleBtn = document.createElement('button');
toggleBtn.innerText = 'Show';
toggleBtn.type = 'button';

toggleBtn.onclick = () => {
    const field = document.getElementById('videoPasswordResult');
    field.type = field.type === 'password' ? 'text' : 'password';
    toggleBtn.innerText = field.type === 'password' ? 'Show' : 'Hide';
};

document.getElementById('videoPasswordResult')?.after(toggleBtn);
