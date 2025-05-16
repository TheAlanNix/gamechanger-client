import pytest
import responses

from gamechanger_client.config import DEFAULT_BASE_DOMAIN
from gamechanger_client.endpoints.clips import ClipsEndpoint
from gamechanger_client.endpoints.me import MeEndpoint
from gamechanger_client.endpoints.organizations import OrganizationsEndpoint
from gamechanger_client.endpoints.players import PlayersEndpoint
from gamechanger_client.endpoints.teams import TeamsEndpoint
from gamechanger_client.http_session import HttpSession


@pytest.fixture
def http_session():
    """Create a test HTTP session."""
    return HttpSession(gc_token="test_token")

@pytest.fixture
def base_url():
    """Get the base URL for API requests."""
    return f"https://{DEFAULT_BASE_DOMAIN}"

class TestTeamsEndpoint:
    @responses.activate
    def test_players(self, http_session, base_url):
        """Test getting team players."""
        team_id = "123"
        responses.add(
            responses.GET,
            f"{base_url}/teams/{team_id}/players",
            json={"players": [{"id": "1", "name": "Player 1"}]},
            status=200
        )

        teams = TeamsEndpoint(http_session)
        response = teams.players(team_id)
        assert response["players"][0]["id"] == "1"

    @responses.activate
    def test_season_stats(self, http_session, base_url):
        """Test getting team season stats."""
        team_id = "123"
        responses.add(
            responses.GET,
            f"{base_url}/teams/{team_id}/season-stats",
            json={"team_id": team_id, "wins": 10, "losses": 5},
            status=200
        )

        teams = TeamsEndpoint(http_session)
        response = teams.season_stats(team_id)
        assert response["team_id"] == team_id
        assert response["wins"] == 10

class TestPlayersEndpoint:
    @responses.activate
    def test_family_relationships(self, http_session, base_url):
        """Test getting player family relationships."""
        player_id = "456"
        responses.add(
            responses.GET,
            f"{base_url}/players/{player_id}/family-relationships",
            json={"relationships": [{"type": "parent", "email": "parent@example.com"}]},
            status=200
        )

        players = PlayersEndpoint(http_session)
        response = players.family_relationships(player_id)
        assert "relationships" in response

class TestClipsEndpoint:
    @responses.activate
    def test_get_clips(self, http_session, base_url):
        """Test getting clips for a team."""
        team_id = "789"
        responses.add(
            responses.GET,
            f"{base_url}/me/clips",
            json={"clips": [{"id": "1", "title": "Test Clip"}]},
            status=200,
            match=[responses.matchers.query_param_matcher({"kind": "event", "teamId": team_id})]
        )

        clips = ClipsEndpoint(http_session)
        response = clips.clips(team_id)
        assert "clips" in response
        assert response["clips"][0]["title"] == "Test Clip"

class TestMeEndpoint:
    @responses.activate
    def test_teams(self, http_session, base_url):
        """Test getting user's teams."""
        responses.add(
            responses.GET,
            f"{base_url}/me/teams",
            json={"teams": [{"id": "1", "name": "Team 1"}]},
            status=200
        )

        me = MeEndpoint(http_session)
        response = me.teams()
        assert "teams" in response
        assert response["teams"][0]["name"] == "Team 1"

    @responses.activate
    def test_user(self, http_session, base_url):
        """Test getting user information."""
        responses.add(
            responses.GET,
            f"{base_url}/me/user",
            json={"id": "123", "name": "Test User", "email": "test@example.com"},
            status=200
        )

        me = MeEndpoint(http_session)
        response = me.user()
        assert response["name"] == "Test User"
        assert response["email"] == "test@example.com"

    @responses.activate
    def test_organizations(self, http_session, base_url):
        """Test getting user's organizations."""
        responses.add(
            responses.GET,
            f"{base_url}/me/organizations",
            json={"organizations": [{"id": "1", "name": "Org 1"}]},
            status=200
        )

        me = MeEndpoint(http_session)
        response = me.organizations()
        assert "organizations" in response
        assert response["organizations"][0]["name"] == "Org 1"

class TestOrganizationsEndpoint:
    @responses.activate
    def test_standings(self, http_session, base_url):
        """Test getting organization standings."""
        org_id = "123"
        responses.add(
            responses.GET,
            f"{base_url}/organizations/{org_id}/standings",
            json={"standings": [{"team_id": "1", "rank": 1}]},
            status=200
        )

        orgs = OrganizationsEndpoint(http_session)
        response = orgs.standings(org_id)
        assert "standings" in response
        assert response["standings"][0]["rank"] == 1

    @responses.activate
    def test_teams(self, http_session, base_url):
        """Test getting organization teams."""
        org_id = "123"
        responses.add(
            responses.GET,
            f"{base_url}/organizations/{org_id}/teams",
            json={"teams": [{"id": "1", "name": "Team 1"}]},
            status=200,
            match=[responses.matchers.query_param_matcher({"page_starts_at": "0"})]
        )

        orgs = OrganizationsEndpoint(http_session)
        response = orgs.teams(org_id)
        assert "teams" in response
        assert response["teams"][0]["name"] == "Team 1"
