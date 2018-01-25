<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Foundation 5</title>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
        integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
        crossorigin="anonymous"></script>
    <link rel="stylesheet"  href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/css/foundation.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/js/foundation.min.js"></script>  
</head>
<body>
    <div class="grid-container">
        <div class="grid-x grid-padding-x">
            <div class="large-12 cell">
                <h1>カレンダーに取り込む君</h1>
                <h4>データ最終更新: ${data['lastUpdate']}</h4>
            </div>
        </div>
        <div class="grid-x grid-padding-x">    
                <form action="/generate" method="post">
                    <button type="button" id="btn-check-all" class="button">すべて選択</button>
                    <button type="button" id="btn-uncheck-all" class="alert button">すべて選択解除</button>
                    <button type="submit"  class="success button">送信</button>
                    %if data:
                        %for i in range(len(data['data'])):
                        <div class="card">
                            <div class="card-divider">
                                <p>${data['data'][i]['title']}</p>
                            </div>
                            <div class="card-section">
                            <p>${data['data'][i]['description'].replace('#nr#','</br>')}</p>

                            <table>
                            <thead>
                                <tr>
                                    <th>詳細</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>場所: ${data['data'][i]['place'].replace('#nr#','</br>')}</td>
                                </tr>
                                <tr>
                                % if data['data'][i]['start_time'] == '00:00' and data['data'][i]['end_time'] == '00:00':
                                    <td>日程: ${data['data'][i]['start_date']}(終日) から ${data['data'][i]['end_date']}(終日)</td>
                                % else:
                                    <td>日程: ${data['data'][i]['start_date']} ${data['data'][i]['start_time']} から ${data['data'][i]['end_date']} ${data['data'][i]['end_time']}</td>
                                % endif
                                </tr>
                            </tbody>
                            </table>
                            <div class="button-group">
                            % if data['data'][i]['link'] != "":
                                <a class="button" href="${data['data'][i]['link']}" >関連サイト</a>
                            % endif
                            </div>
                            <input id="event${i+1}" type="checkbox" name="event${i+1}" value="${data['data'][i]['title']}"><label for="event${i+1}">取り込む</label>
                            </div>
                        </div>
                        %endfor
                    %endif
                    </tbody>
                    </table>
                </form>
            </div>
        </div>
    </div>
<script type="text/javascript">
$(function() {
    $('#btn-check-all').click(function(e) {
        for(var i=0; i<${len(data['data'])}; i++) {
            console.log("event" + (i+1));
            $("#event" + (i+1)).prop("checked",true);
        }
    });
    $('#btn-uncheck-all').click(function(e) {
        for(var i=0; i<${len(data['data'])}; i++) {
            console.log("event" + (i+1));
            $("#event" + (i+1)).prop("checked",false);
        }
    });
});
</script>
</body>
</html>