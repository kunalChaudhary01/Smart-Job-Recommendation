// Smart Job Recommendation System - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebarToggle && sidebar && sidebarOverlay) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            sidebarOverlay.classList.toggle('show');
        });

        sidebarOverlay.addEventListener('click', function () {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }

    // 2. Password Visibility Toggle
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                const isPassword = targetInput.getAttribute('type') === 'password';
                targetInput.setAttribute('type', isPassword ? 'text' : 'password');
                const icon = this.querySelector('i');
                if (icon) {
                    if (isPassword) {
                        icon.classList.remove('bi-eye');
                        icon.classList.add('bi-eye-slash');
                    } else {
                        icon.classList.remove('bi-eye-slash');
                        icon.classList.add('bi-eye');
                    }
                }
            }
        });
    });

    // 3. Auto-dismiss Flash Messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(30px)';
            msg.style.transition = 'all 0.5s ease-out';
            setTimeout(function () {
                msg.remove();
            }, 500);
        }, 5000);
    });

    // 4. Drag & Drop File Upload Zones
    const uploadZones = document.querySelectorAll('.upload-zone');
    uploadZones.forEach(function (zone) {
        const fileInput = zone.querySelector('input[type="file"]') || document.getElementById('resumeFileInput') || document.querySelector('input[name="resume"]');
        const fileInfo = zone.querySelector('.file-info') || document.getElementById('fileInfoArea');
        const fileNameDisplay = zone.querySelector('.file-name-display') || document.getElementById('selectedFileName');
        const fileSizeDisplay = zone.querySelector('.file-size-display') || document.getElementById('selectedFileSize');
        const submitBtn = zone.querySelector('.upload-submit-btn') || document.getElementById('uploadSubmitBtn');

        if (!fileInput) return;

        function updateFileInfo(file) {
            if (!file) return;
            if (fileNameDisplay) {
                fileNameDisplay.textContent = file.name;
            }
            if (fileSizeDisplay) {
                const sizeKb = (file.size / 1024).toFixed(1);
                const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
                fileSizeDisplay.textContent = file.size > 1024 * 1024 ? `${sizeMb} MB` : `${sizeKb} KB`;
            }
            if (fileInfo) {
                fileInfo.classList.remove('d-none');
            }
            if (submitBtn) {
                submitBtn.classList.remove('d-none');
            }
        }

        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                updateFileInfo(this.files[0]);
            }
        });

        zone.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.stopPropagation();
            zone.classList.add('drag-active');
        });

        zone.addEventListener('dragleave', function (e) {
            e.preventDefault();
            e.stopPropagation();
            zone.classList.remove('drag-active');
        });

        zone.addEventListener('drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
            zone.classList.remove('drag-active');

            if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                updateFileInfo(e.dataTransfer.files[0]);
            }
        });
    });
});
