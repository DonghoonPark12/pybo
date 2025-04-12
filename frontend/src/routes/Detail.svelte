<script>
    import fastapi from "../lib/api";
    import {get} from "svelte/store";
    import Error from "../components/Error.svelte";
    import { link, push } from "svelte-spa-router"
    import { is_login, username } from "../lib/store"
    import { marked } from "marked";
    import moment from 'moment/min/moment-with-locales'
    import Button from "bootstrap/js/src/button.js";
    moment.locales('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[], voter:[], content: ''}
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

    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function delete_answer(answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
    function vote_question(_question_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/question/vote"
            let params = {
                question_id: _question_id
            }
            fastapi('post', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>


<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
           <div class="card-text">{@html marked.parse(question.content)}</div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date }
                    <div class="badge bg-light text-dark p-2 text-start mx-3">
                        <div class="mb-2">modified at</div>
                        <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                    </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click="{vote_question(question.id)}">
                    추천
                    <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
                </button>
                <!-- 질문 수정 링크는 로그인한 사용자와 글쓴이가 같은 경우에만 보여야 하므로-->
                {#if question.user && $username === question.user.username }
                <a use:link href="/question-modify/{question.id}"
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
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
                <div class="card-text">{@html marked.parse(answer.content)}</div>
                <div class="d-flex justify-content-end">
                    {#if answer.modify_date }
                        <div class="badge bg-light text-dark p-2 text-start mx-3">
                            <div class="mb-2">modified at</div>
                            <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                        </div>
                    {/if}
                    <div class="badge bg-light text-dark p-2 text-start">
                        <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                        <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                    </div>
                </div>
                <div class="my-3">
                    {#if answer.user && $username === answer.user.username }
                    <a use:link href="/answer-modify/{answer.id}"
                        class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary"
                        on:click={() => delete_answer(answer.id) }>삭제</button>
                    {/if}
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