$( document ).ready(function() {
    // Show #mcr-input-group on Linux/Mac only
    if (! navigator.platform.includes('Win')) {
        $("#mcr-input-group").show();
    }

    // Call into Python to load settings file (if it exists)
    async function load_settings() {
        var spm12_path = await eel.load_settings()();
        if (spm12_path) {
            $('#spm-path-input').val(spm12_path);
        }
    }
    load_settings()

    // Call into Python to save settings
    async function save_settings(spm12_path) {
        eel.save_settings(spm12_path)();
    }
    $('#save-settings').click(function(){
        var spm12_path = $('#spm-path-input').val();
        save_settings(spm12_path)
    });

    // Call into Python to get dir selector
    async function get_output_folder() {
        var output_path = await eel.get_folder()();
          if (output_path) {
            $('#output-path-input').val(output_path);
          }
      }

    // Call into Python to get nii file selector
    async function get_nii_file(selector) {
        var file_path = await eel.get_nii_file()();
          if (file_path) {
            $(selector).val(file_path);
          }
      }

    // Call into Python to get SPM12 selector
    async function get_spm_bin(selector) {
        var spm12_path = await eel.get_spm_bin()();
        if (spm12_path) {
            $('#spm-path-input').val(spm12_path);
          }
        }

    // Get SPM12 path on click
    $('#spm-path').click(function(){
        get_spm_bin()
    });

    // Get T1 MRI path on click
    $('#t1-mri').click(function(){
        get_nii_file('#t1-mri-input')
    });

    // Get interictal SPECT path on click
    $('#interictal-spect').click(function(){
        get_nii_file('#interictal-spect-input')
    });

    // Get ictal SPECT path on click
    $('#ictal-spect').click(function(){
        get_nii_file('#ictal-spect-input')
    });

    // Get output dir path on click
    $('#output-path').click(function(){
        get_output_folder()
    });

});