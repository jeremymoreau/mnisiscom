$(document).ready(function() {
  // SISCOM threshold
  var siscom_threshold_slider = document.getElementById("siscom-threshold");
  noUiSlider.create(siscom_threshold_slider, {
    start: [0.5],
    connect: false,
    range: {
      min: 0,
      max: 1
    }
  });
  siscom_threshold_slider.noUiSlider.on("update", function() {
    siscom_threshold = siscom_threshold_slider.noUiSlider.get();
    document.getElementById("siscom-threshold-label").textContent =
      "SISCOM threshold (" + siscom_threshold + "):";
  });

  // Mask threshold
  var mask_threshold_slider = document.getElementById("mask-threshold");
  noUiSlider.create(mask_threshold_slider, {
    start: [0.6],
    connect: false,
    range: {
      min: 0,
      max: 1
    }
  });
  mask_threshold_slider.noUiSlider.on("update", function() {
    mask_threshold = mask_threshold_slider.noUiSlider.get();
    document.getElementById("mask-threshold-label").textContent =
      "Mask threshold (" + mask_threshold + "):";
  });

  // Slice thickness
  var slice_thickness_slider = document.getElementById(
    "slice-thickness-slider"
  );
  noUiSlider.create(slice_thickness_slider, {
    start: [5],
    connect: false,
    step: 1,
    range: {
      min: 1,
      max: 20
    }
  });
  slice_thickness_slider.noUiSlider.on("update", function() {
    slice_thickness = slice_thickness_slider.noUiSlider.get();
    document.getElementById("slice-thickness-label").textContent =
      "Slice thickness (" + Math.round(slice_thickness) + " voxels):";
  });

  // Overlay transparency
  var transparency_slider = document.getElementById("transparency-slider");
  noUiSlider.create(transparency_slider, {
    start: [0.8],
    connect: false,
    range: {
      min: 0,
      max: 1
    }
  });
  transparency_slider.noUiSlider.on("update", function() {
    transparency = transparency_slider.noUiSlider.get();
    document.getElementById("transparency-slider-label").textContent =
      "Overlay transparency (" + transparency + "):";
  });

  // MRI Window
  var mri_window_slider = document.getElementById("mri-window-slider");
  noUiSlider.create(mri_window_slider, {
    start: [0.1, 0.9],
    connect: true,
    range: {
      min: 0,
      max: 1
    }
  });
  mri_window_slider.noUiSlider.on("update", function() {
    mri_window = mri_window_slider.noUiSlider.get();
    document.getElementById("mri-window-label").textContent =
      "MRI Window (" + mri_window[0] + " - " + mri_window[1] + "):";
  });

  // SPECT Window
  var spect_window_slider = document.getElementById("spect-window-slider");
  noUiSlider.create(spect_window_slider, {
    start: [0, 4.5],
    connect: true,
    range: {
      min: 0,
      max: 10
    }
  });
  spect_window_slider.noUiSlider.on("update", function() {
    spect_window = spect_window_slider.noUiSlider.get();
    document.getElementById("spect-window-label").textContent =
      "SPECT Window (" + spect_window[0] + " - " + spect_window[1] + " stdev):";
  });

  // SISCOM Window
  var siscom_window_slider = document.getElementById("siscom-window-slider");
  noUiSlider.create(siscom_window_slider, {
    start: [0, 2],
    connect: true,
    range: {
      min: 0,
      max: 10
    }
  });
  siscom_window_slider.noUiSlider.on("update", function() {
    siscom_window = siscom_window_slider.noUiSlider.get();
    document.getElementById("siscom-window-label").textContent =
      "SISCOM Window (" +
      siscom_window[0] +
      " - " +
      siscom_window[1] +
      " stdev):";
  });
});
