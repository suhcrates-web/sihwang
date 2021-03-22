

$(document).ready(function(){
	
	$(document).on('click', '#make_box', function(event){
		
		// alert('shit')
		// var clicked = this.id
		// if(clicked != 'avoid'){
		// $(this).siblings('tr').removeClass('onclick')
		// $(this).addClass('onclick')
		$('#make_box').html("생성중....(10초 소요됨)")
		$.ajax({
			data:{
				cmd : "giveme",
			},
			type : 'POST',
			url : '/sihwang_post'
		})
		.done(function(data){
			if (data['cmd'] =='not_yet'){
				$('#make_box').html("생성버튼")
				alert(data.message)}
			else if (data['cmd'] =='ok'){
				$('#content_box').html(data.message)
				$('#now').html(data.time)
				$('#make_box').html("생성완료~~")
			}
		});

		
	});
});



$(document).ready(function(){


	$(document).on('click', '.nextto', function(event){
		var clicked = this.id
		var name = this.textContent
		if (confirm("시황당번을 ["+name+"]으로 바꾸시겠습니까?")){
			$.ajax({
			data:{
				cmd : "change",
				id : clicked
			},
			type : 'POST',
			url : '/change_dangbun'
		})
		.done(function(data){
			$('#'+clicked).siblings('div').removeClass('dangbun')
			$('#'+clicked).addClass("dangbun")

		})
		
		}else{
			console.log("ok")	
		}
	})
});