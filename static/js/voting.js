function vote(inId, inVoteValueStr) {
        $.ajax(
            {url: "/vote/" + inId + "/" + inVoteValueStr, success: function(){

                var voteSpan = $('#voteSpan_' + inId);
                var originalScore = Number(voteSpan.data('original-score'));

                if (inVoteValueStr === 'upvote')
                    var currentBtn = $('#upvoteButton_' + inId);
                else
                    var currentBtn = $('#downvoteButton_' + inId);

                var clicked = (currentBtn.hasClass('upvoted') || currentBtn.hasClass('downvoted')) ? true : false;

                $('#upvoteButton_' + inId).removeClass('upvoted');
                $('#downvoteButton_' + inId).removeClass('downvoted');

                if (clicked)
                {
                    voteSpan.text(originalScore);
                    return;
                }
                switch (inVoteValueStr)
                {
                    case 'upvote':
                        voteSpan.text(originalScore + 1);
                        currentBtn.addClass('upvoted');
                    break;

                    case 'downvote':
                        currentBtn.addClass('downvoted');

                        if (originalScore === 0)
                        {
                            voteSpan.text(0);
                        }
                        else
                        {
                            voteSpan.text(originalScore - 1);
                        }
                    break;
                }

        }});
      }
