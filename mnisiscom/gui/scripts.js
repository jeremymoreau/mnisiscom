$( document ).ready(function() {
    // Show #mcr-input-group on Linux/Mac only
    if (! navigator.platform.includes('Win')) {
        $("#mcr-input-group").show();
    }

    // Call into Python to load settings file (if it exists)
    async function load_settings() {
        var mnisiscom_settings = await eel.load_settings()();
        if (mnisiscom_settings) {
            var spm12_path = mnisiscom_settings[0]
            var mcr_path = mnisiscom_settings[1]
            $('#spm-path-input').val(spm12_path);
            $('#mcr-path-input').val(mcr_path);
        }
    }
    load_settings()

    // Call into Python to save settings
    async function save_settings(spm12_path, mcr_path) {
        eel.save_settings(spm12_path, mcr_path)();
    }
    $('#save-settings').click(function(){
        var spm12_path = $('#spm-path-input').val();
        var mcr_path = $('#mcr-path-input').val();
        save_settings(spm12_path, mcr_path)
    });

    // Call into Python to get dir selector
    async function get_output_folder() {
        var output_path = await eel.get_folder()();
          if (output_path) {
            $('#output-path-input').val(output_path);
          }
      }
    
    // Call into Python to get MCR dir selector
    async function get_mcr_folder() {
        var mcr_dir_path = await eel.get_mcr_folder()();
          if (mcr_dir_path) {
            if (mcr_dir_path === 'Invalid MCR folder.') {
                $('#invalid-mcr-alert').fadeIn(800);
            } else {
                $('#mcr-path-input').val(mcr_dir_path);
                $('#invalid-mcr-alert').fadeOut(800);
            }
          }
      }
    $('#mcr-path').click(function(){
        get_mcr_folder();
    });

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

    // Run mnisiscom on click
    $('#compute-button').click(function(){
        // Get file paths
        var t1_mri_path = $('#t1-mri-input').val()
        var interictal_spect_path = $('#interictal-spect-input').val()
        var ictal_spect_path = $('#ictal-spect-input').val()
        var output_path = $('#output-path-input').val()

        // Get checkbox values
        var skip_coreg = $('#skip-coreg').is(':checked');
        var mri_panel = $('#mri-panel').is(':checked');
        var glass_brain = $('#glass-brain').is(':checked');

        // Get settings
        var spm12_path = $('#spm-path-input').val();
        var mcr_path = $('#mcr-path-input').val();

        // Save all params in a dict
        param_dict = {
            't1_mri_path': t1_mri_path,
            'interictal_spect_path': interictal_spect_path,
            'ictal_spect_path': ictal_spect_path,
            'output_path': output_path,
            'siscom_threshold': siscom_threshold,
            'mask_threshold': mask_threshold,
            'slice_thickness': slice_thickness,
            'overlay_transparency': transparency,
            'mri_window': mri_window,
            'spect_window': spect_window,
            'siscom_window': siscom_window,
            'skip_coreg': skip_coreg,
            'mri_panel': mri_panel,
            'glass_brain': glass_brain,
            'spm12_path': spm12_path,
            'mcr_path': mcr_path
        }

        // Check that all required params have been inputted
        // Get array of missing params
        var missing_params_array = []
        for (var key in param_dict){
            var value = param_dict[key];

            // Don't check for mcr_path on Windows
            if ( navigator.platform.includes('Win') ) {
                if ( key !== 'mcr_path') {
                    // If no value set (exclude boolean checkboxes)
                    if ( ! value && typeof value !== 'boolean') {
                        missing_params_array.push(key)
                    };
                };

            // Mac or Linux
            } else {
                // If no value set (exclude boolean checkboxes)
                if ( ! value && typeof value !== 'boolean') {
                    missing_params_array.push(key)
                };
            };

          };
        
        // Display error message if there are any missing params
        if ( missing_params_array.length !== 0) {
            $('#error-modal-body').empty()  // Empty error modal in case it was previously called
            $('#error-modal').modal('show');
            for ( var missing_param_i in missing_params_array) {
                var missing_param = missing_params_array[missing_param_i].replace(/_/g, ' ')
                
                $('#error-modal-body').append(
                    `
                    <div class="alert alert-danger" role="alert">
                        <span class="alert-inner--text"><strong>Error!</strong><span class="ml-2">Please make sure to select a value for: <strong>${missing_param}</strong></span></span>
                    </div>
                    `
                    );
            };

        // Compute results
        } else {
            // TODO: call mnisiscom
            console.log('Run!')
        };


    });
});