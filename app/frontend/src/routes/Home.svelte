<script>
    import fastapi from "../lib/api.js"
    import {link} from 'svelte-spa-router'
    import {page, keyword, is_login} from '../lib/store.js'
    import moment from 'moment/min/moment-with-locales'
    moment.locales('ko')

    let question_list = []
    let size = 10
    //let page = 0
    let total = 0
    let kw = ''

    // 스벨트에서 변수앞에 $: 기호를 붙이면 해당 변수는 반응형 변수가 된다.
    // total 변수의 값이 API 호출로 인해 그 값이 변하면 total_page 변수의 값도 실시간으로 재 계산된다는 의미이다.
    $: total_page = Math.ceil(total / size)
    $: get_question_list($page)

    function get_question_list(_page) {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }

        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
            kw = $keyword
        })

        // success_callback 함수를 화살표 함수로 작성하여 전달
        // 화살표 함수의 내용은 응답으로 받은 json 데이터를 question_list에 대입하라는 내용이다.

        // fetch("http://127.0.0.1:8000/api/question/list").then((response) => {
        //     response.json().then((json) => {
        //         question_list = json
        //     })
        // })
    }
    // 위와 같이 $: 변수1, 변수2, 자바스크립트식 과 같이 사용하면 스벨트는
    // "변수1" 또는 "변수2"의 값이 변경되는지를 감시하다가 값이 변경되면 자동으로 "자바스크립트식"을 실행
    $: $page, $keyword, get_question_list()
    //$: get_question_list($page)
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
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/question-create"
                class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
                    찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
            <tr class="text-center table-dark">
                <th>번호</th>
                <th style="width:50%">제목</th>
                <th>글쓴이</th>
                <th>작성일시</th>
            </tr>
        </thead>

        <tbody>
            {#each question_list as question, i}
                <tr class="text-center">
                    <td>{ total - ($page * size) - i }</td>
                    <td class="text-start">
                        <a use:link href="/detail/{question.id}">{question.subject}</a>
                        {#if question.answers.length > 0 }
                            <span class="text-danger small mx-2">{question.answers.length}</span>
                        {/if}
                    </td>
                    <td>{ question.user ? question.user.username : "" }</td>
                    <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
                </tr>
            {/each}
        </tbody>
    </table>

    <!--    https://getbootstrap.com/docs/5.2/components/pagination/-->
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">Previous</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
            <!--    {#if loop_page >= page && loop_page <= page+5}-->
            {#if loop_page >= Math.floor($page/6) * 6 && loop_page < Math.floor($page/6) * 6 + 6}
            <li class="page-item {loop_page === $page && 'active'}">
                <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
            </li>
            {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">Next</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->
<!--    <a use:link href="/question-create"-->
<!--       class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>-->
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
