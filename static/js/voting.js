function vote(inId, inVoteValueStr) {
        $.ajax(
            {url: "/vote/" + inId + "/" + inVoteValueStr, success: function(){

                if (inVoteValueStr === 'upvote')
                    voteInt = 1;
                else
                    voteInt = -1;

                const voteSpan = $('#vote_' + inId);
                const currentAmount = parseInt(voteSpan.text());
                voteSpan.text(currentAmount + voteInt);
        }});
      }

$( ".voteSpan" ).each(function() {
  const voteSpan = $( this );
  $.ajax(
    {url: "/votecount/" + voteSpan.data('db'), success: function( result ){
        voteSpan.text( result );
  }});
});