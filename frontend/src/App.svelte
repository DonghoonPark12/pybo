<script>
    let message, promise;

    fetch("http://127.0.0.1:8000/hello").then(response => {
        response.json().then(json => {
            message = json.message;
        })
    });

    // async function hello() {
    //     const res = await fetch("http://127.0.0.1:8000/hello");
    //     const json = await res.json();
    //
    //     if (res.ok) {
    //       return json.message;
    //     } else {
    //       alert("error");
    //     }
    // }
    //
    // promise = hello();
</script>

<!--{#await promise}-->
<!--  <p>...waiting</p>-->
<!--{:then message}-->
<!--  <h1>{message}</h1>-->
<!--{/await}-->

<h1>{message}</h1>

<!--
<script> 블록에 message라는 변수를 생성하고 FastAPI의 hello API를 호출하여 돌려받은 값을 message 변수에 담았다.
그리고 담겨진 message 값은 <h1>{message}</h1>로 출력했다.
Svelte는 자바스크립트에 선언된 변수의 값을 HTML 태그에 중괄호 기호를 사용하여 표시할 수 있다.
https://ko.javascript.info/fetch
-->