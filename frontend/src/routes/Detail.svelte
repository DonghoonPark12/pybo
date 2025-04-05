<script>
    import fastapi from "../lib/api";
    import {get} from "svelte/store";
    import Error from "../components/Error.svelte";
    import { push } from "svelte-spa-router"
    import { is_login } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locales('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question() {
        fastapi('get', '/api/question/detail/' + question_id, {}, (json) => {
            question = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content
        }
        fastapi('post', url, params,
            (json) => {
                content = ""
                error = {detail:[]}
                get_question()
            },
            (err_json) => {
                error = err_json
            }
        )
    }
</script>


<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                </div>
            </div>
        </div>
    </div>

    <button class="btn btn-secondary" on:click="{() => {
        push('/')
    }}"> 목록으로 </button>

    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
                <div class="d-flex justify-content-end">
                    <div class="badge bg-light text-dark p-2">
                        {moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                    </div>
                </div>
            </div>
        </div>
    {/each}
    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} disabled={$is_login ? "" : "disabled"} class="form-control"></textarea>
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{post_answer}" />
    </form>
</div>


<!--<h1>{question.subject}</h1>-->

<!--<div>-->
<!--    {question.content}-->
<!--</div>-->

<!--<ul>-->
<!--    {#each question.answers as answer}-->
<!--        <li>{answer.content}</li>-->
<!--    {/each}-->
<!--</ul>-->

<Error error={error} />

<!--<form method="post">-->
<!--    <textarea rows="15" bind:value={content}></textarea>-->
<!--    <input type="submit" value="답변등록" on:click="{post_answer}">-->
<!--</form>-->

<!--<style>-->
<!--    textarea {width: 100%;}-->
<!--    input[type=submit] {margin-top: 10px;}-->
<!--</style>-->


<!--
FE와 BE의 연결)

답변 등록을 위한 <form> 엘리먼트를 추가
textarea에 답변 내용을 적고 "답변등록" 버튼을 누르면 답변이 등록되어야 한다.
텍스트 창에 작성한 내용은 스크립트 영역에 추가한 content 변수와 연결되도록 bind:value={content} 속성을 사용
textarea에 값을 추가하거나 변경할 때마다 content의 값도 자동으로 변경될 것이다.

"답변등록" 버튼을 누르면 post_answer 함수가 호출되도록 on:click="{post_answer}" 속성을 추가
textarea에 작성한 content를 파라미터로 답변 등록 API를 호출
답변 등록이 성공하면 등록한 답변이 textarea에서 지워지도록 content에 빈 문자열을 대입
event.preventDefault()는 submit 버튼이 눌릴경우 form이 자동으로 전송되는 것을 방지하기 위해 사용
-->