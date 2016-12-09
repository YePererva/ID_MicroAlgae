$(function () {
      var $select = document.getElementById("selected");
      var $whole = document.getElementById("whole")
      var $image = $('#input_image');

      $image.cropper({
          build: function (e) {
            var $clone = $(this).clone();
            $clone.css({
              display: 'block',
              width: '100%',
              minWidth: 0,
              minHeight: 0,
              maxWidth: 'none',
              maxHeight: 'none'
            });
            $select.checked = false;
            $whole.checked = true;
          },         

          built: function(e) {
            $(this).cropper('clear');
            $whole.checked = true;
            $select.checked = false;
            $select.disabled = true;
          },

          crop: function(e) {
            $(this).cropper()
            document.getElementById("selected_info").value = [e.x, e.y, e.width, e.height];  
            
            if (e.width == 0) {
              // if no selection on image
              $whole.checked = true;
              $select.disabled = true;
              $select.checked = false;
            } else {
              // if part of image is selected
              $whole.checked = false;
              $select.disabled = false;
              $select.checked = true;
              };

            },
        });

      $('#clear').on('click', function () {
        $image.cropper('clear');
        $select.disabled = true;
        $whole.checked =true;
      });

      $('#original').on('click', function () {
        $image.cropper('reset', true);
        $image.cropper('clear');
        $select.disabled = true;
        $whole.checked =true;
      });

    });