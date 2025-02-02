<script>
    import fastapi from "../lib/api"
    import {link} from 'svelte-spa-router'

    let question_list = []

    function get_question_list() {
        fastapi('get', '/api/question/list', {}, (json) => {question_list = json})

        // success_callback 함수를 화살표 함수로 작성하여 전달
        // 화살표 함수의 내용은 응답으로 받은 json 데이터를 question_list에 대입하라는 내용이다.

        // fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
        //     response.json().then((json) => {
        //         question_list = json
        //     })
        // })
    }

    get_question_list()
    // let message, promise;

    // fetch("http://127.0.0.1:8000/hello").then(response => {
    //     response.json().then(json => {
    //         message = json.message;
    //     })
    // });

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

<div class="container my-3">
    <table class="table">
        <thead>
            <tr class="table-dark">
                <th>번호</th>
                <th>제목</th>
                <th>작성일시</th>
            </tr>
        </thead>

        <tbody>
            {#each question_list as question, i}
                <tr>
                    <td>{i+1}</td>
                    <td> <a use:link href="/detail/{question.id}">{question.subject}</a> </td>
                    <td>{question.create_date}</td>
                </tr>
            {/each}
        </tbody>

    </table>
</div>

<!--&lt;!&ndash;<h1>{message}</h1>&ndash;&gt;-->
<!--<ul>-->
<!--    {#each question_list as question}-->
<!--&lt;!&ndash;        <li>{question.subject}</li>&ndash;&gt;-->
<!--        <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>-->
<!--    {/each}-->
<!--</ul>-->


<!--a 태그에 use:link 를 사용하는 이유
 - 사용 방법
    - <a href="/some-path">Some Path</a>
    - 위와 같은 링크를 클릭하면 브라우저 주소창에 다음과 같이 표시된다.
    - http://127.0.0.1:5173/some-path

 - 이번에는 다음처럼 a 태그에 use:link를 사용할 경우
    - <a use:link href="/some-path">Some Path</a>
    - 위와 같은 링크를 클릭하면 브라우저 주소창에 다음과 같이 표시된다.
    - http://127.0.0.1:5173/#/some-path

 - use:link 속성을 사용한 경우는 항상 /# 문자가 선행되도록 경로가 만들어진다.
 - 웹 페이지에서 어떤 경로가 /#으로 시작하면 브라우저는 이 경로를 하나의 페이지로 인식한다.

 - 즉, 브라우저는 http://127.0.0.1:5173/#/some-path,
 - http://127.0.0.1:5173/#/question-create 두 개의 경로를 모두 동일한 페이지로 인식한다는 점이다.
 - 이러한 것을 해시 기반 라우팅(hash based routing)이라고 한다.
-->
