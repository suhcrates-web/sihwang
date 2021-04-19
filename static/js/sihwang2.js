

$(document).ready(function(){
	
	$(document).on('click', '#make_box', function(event){
		var state = this.getAttribute("state");
		
		// alert('shit')
		// var clicked = this.id
		// if(clicked != 'avoid'){
		// $(this).siblings('tr').removeClass('onclick')
		// $(this).addClass('onclick')
		$('#make_box').html("생성중....(10초 소요됨)")
		$.ajax({
			data:{
				cmd : "giveme",
				version : "2",
				state: state
			},
			type : 'POST',
			url : '/sihwang_post2'
		})
		.done(function(data){
			if (data['cmd'] =='not_yet'){
				$('#make_box').html("생성버튼")
				location.reload()
				alert(data.message)}
			else if (data['cmd'] =='ok'){
				$('#content_box').html(data.message)
				$('#now').html(data.time)
				$('#make_box').html("생성완료~~")
				
			}
		});

		
	});
});


