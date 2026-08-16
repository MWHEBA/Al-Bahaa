/**
 * Job Detail Page - Premium Drag & Drop Resume Upload
 */

document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('cv-dropzone');
  const fileInput = document.getElementById('id_resume');
  const idleState = document.getElementById('cv-dropzone-idle');
  const attachedState = document.getElementById('cv-dropzone-attached');
  const fileNameEl = document.getElementById('cv-file-name');
  const removeBtn = document.getElementById('cv-file-remove');

  if (!dropzone || !fileInput) return;

  function updateFileDisplay(file) {
    if (file) {
      fileNameEl.textContent = file.name;
      idleState.style.display = 'none';
      attachedState.style.display = 'flex';
      dropzone.classList.add('has-file');
    } else {
      fileInput.value = '';
      fileNameEl.textContent = '';
      idleState.style.display = 'flex';
      attachedState.style.display = 'none';
      dropzone.classList.remove('has-file');
    }
  }

  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  // Highlight dropzone on drag over
  ['dragenter', 'dragover'].forEach((eventName) => {
    dropzone.addEventListener(eventName, () => {
      dropzone.classList.add('is-dragover');
    });
  });

  ['dragleave', 'dragend', 'drop'].forEach((eventName) => {
    dropzone.addEventListener(eventName, () => {
      dropzone.classList.remove('is-dragover');
    });
  });

  // Handle dropped files
  dropzone.addEventListener('drop', (e) => {
    const droppedFiles = e.dataTransfer?.files;
    if (droppedFiles && droppedFiles.length > 0) {
      const file = droppedFiles[0];
      const validExtensions = ['.pdf', '.doc', '.docx'];
      const fileExt = '.' + file.name.split('.').pop().toLowerCase();

      if (validExtensions.includes(fileExt)) {
        // Assign to the file input via DataTransfer
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        updateFileDisplay(file);
      } else {
        alert('Please upload a valid PDF or Word document (.pdf, .doc, .docx)');
      }
    }
  });

  // Handle standard file picker selection
  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files.length > 0) {
      updateFileDisplay(fileInput.files[0]);
    } else {
      updateFileDisplay(null);
    }
  });

  // Handle file remove button
  if (removeBtn) {
    removeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      updateFileDisplay(null);
    });
  }
});
