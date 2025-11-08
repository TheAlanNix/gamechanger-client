import pytest
import responses

from gamechanger_client.config import DEFAULT_BASE_DOMAIN
from gamechanger_client.endpoints.clips import ClipsEndpoint
from gamechanger_client.endpoints.me import MeEndpoint
from gamechanger_client.endpoints.organizations import OrganizationsEndpoint
from gamechanger_client.endpoints.players import PlayersEndpoint
from gamechanger_client.endpoints.search import SearchEndpoint
from gamechanger_client.endpoints.teams import TeamsEndpoint
from gamechanger_client.http_session import HttpSession
from gamechanger_client.exceptions import SchemaValidationError


@pytest.fixture
def http_session():
    """Create a test HTTP session."""
    return HttpSession(gc_token="test_token")

@pytest.fixture
def base_url():
    """Get the base URL for API requests."""
    return f"https://{DEFAULT_BASE_DOMAIN}"


class TestTeamsEndpoint:
    """Test the TeamsEndpoint class with hybrid approach functionality."""

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

    @responses.activate
    def test_create_team_basic(self, http_session, base_url):
        """Test creating a team with basic parameters."""
        responses.add(
            responses.POST,
            f"{base_url}/teams",
            json={"team": {"id": "new_team_123", "name": "Test Team"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create(
            name="Test Team",
            sport="baseball",
            city="Atlanta",
            state="GA",
            country="USA",
            season_name="Spring",
            season_year=2025,
            age_group="U12",
            competition_level="Recreational"
        )
        
        assert response["team"]["name"] == "Test Team"

    @responses.activate  
    def test_create_team_with_additional_fields(self, http_session, base_url):
        """Test creating a team with additional fields."""
        responses.add(
            responses.POST,
            f"{base_url}/teams",
            json={"team": {"id": "new_team_124", "name": "Advanced Team"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create(
            name="Advanced Team",
            sport="baseball",
            city="Atlanta",
            state="GA", 
            country="USA",
            season_name="Spring",
            season_year=2025,
            age_group="U12",
            competition_level="Recreational",
            additional_fields={
                "logo_url": "https://example.com/logo.png",
                "sponsor": "Local Business"
            },
            custom_field="custom_value"
        )
        
        assert response["team"]["name"] == "Advanced Team"

    @responses.activate
    def test_create_event_basic(self, http_session, base_url):
        """Test creating an event with basic parameters."""
        team_id = "123"
        responses.add(
            responses.POST,
            f"{base_url}/teams/{team_id}/schedule/events/",
            json={"event": {"id": "event_456", "title": "Practice"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create_event(
            team_id=team_id,
            event_type="practice",
            status="confirmed",
            start_time="2025-04-01T10:00:00Z",
            end_time="2025-04-01T12:00:00Z",
            arrive_time="2025-04-01T09:45:00Z",
            location="Field 1"
        )
        
        assert response["event"]["id"] == "event_456"

    @responses.activate
    def test_create_event_with_additional_fields(self, http_session, base_url):
        """Test creating an event with additional fields."""
        team_id = "123" 
        responses.add(
            responses.POST,
            f"{base_url}/teams/{team_id}/schedule/events/",
            json={"event": {"id": "event_457", "title": "Game vs Rivals"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create_event(
            team_id=team_id,
            event_type="game",
            status="confirmed", 
            start_time="2025-04-05T14:00:00Z",
            end_time="2025-04-05T16:00:00Z",
            arrive_time="2025-04-05T13:30:00Z",
            location="Main Field",
            title="Championship Game",
            opponent_id="rival_team_789",
            opponent_name="Rival Team",
            additional_fields={
                "broadcast_url": "https://stream.example.com/game1",
                "weather_backup": "Indoor facility"
            },
            special_instructions="Bring extra water"
        )
        
        assert response["event"]["title"] == "Game vs Rivals"

    @responses.activate
    def test_create_player_basic(self, http_session, base_url):
        """Test creating a player with basic parameters."""
        team_id = "123"
        responses.add(
            responses.POST,
            f"{base_url}/teams/{team_id}/players/",
            json={"player": {"id": "player_789", "first_name": "John"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create_player(
            team_id=team_id,
            first_name="John", 
            last_name="Doe",
            number=42
        )
        
        assert response["player"]["first_name"] == "John"

    @responses.activate
    def test_create_player_with_additional_fields(self, http_session, base_url):
        """Test creating a player with additional fields."""
        team_id = "123"
        responses.add(
            responses.POST,
            f"{base_url}/teams/{team_id}/players/",
            json={"player": {"id": "player_790", "first_name": "Jane"}},
            status=201
        )

        teams = TeamsEndpoint(http_session)
        response = teams.create_player(
            team_id=team_id,
            first_name="Jane",
            last_name="Smith", 
            number=24,
            batting_side="left",
            throwing_hand="right",
            additional_fields={
                "parent_email": "parent@example.com",
                "emergency_contact": "555-0123"
            },
            position="shortstop"
        )
        
        assert response["player"]["first_name"] == "Jane"

    @responses.activate
    def test_delete_team_with_params(self, http_session, base_url):
        """Test deleting a team with additional parameters."""
        team_id = "123"
        responses.add(
            responses.DELETE,
            f"{base_url}/teams/{team_id}",
            body="Team deleted successfully",
            status=200
        )

        teams = TeamsEndpoint(http_session)
        response = teams.delete(
            team_id=team_id,
            additional_params={"reason": "season_ended"},
            force=True
        )
        
        assert "deleted successfully" in response

    @responses.activate
    def test_delete_event(self, http_session, base_url):
        """Test deleting an event with additional fields."""
        team_id = "123"
        event_id = "event_456"
        responses.add(
            responses.PATCH,
            f"{base_url}/teams/{team_id}/schedule/events/{event_id}",
            json={"event": {"id": event_id, "status": "canceled"}},
            status=200
        )

        teams = TeamsEndpoint(http_session)
        response = teams.delete_event(
            team_id=team_id,
            event_id=event_id,
            should_notify=True,
            message="Weather cancellation",
            additional_fields={"reason_code": "WEATHER"},
            refund_eligible=True
        )
        
        assert response["event"]["status"] == "canceled"


class TestPlayersEndpoint:
    """Test the PlayersEndpoint class with hybrid approach functionality."""

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

    @responses.activate
    def test_update_family_relationships_basic(self, http_session, base_url):
        """Test updating family relationships with basic parameters."""
        player_id = "456"
        responses.add(
            responses.PATCH,
            f"{base_url}/players/{player_id}/family-relationships",
            json={"updated": True, "relationships_count": 2},
            status=200
        )

        players = PlayersEndpoint(http_session)
        response = players.update_family_relationships(
            player_id=player_id,
            action="add",
            entities=["parent@example.com", "guardian@example.com"]
        )
        
        assert response["updated"] is True

    @responses.activate
    def test_update_family_relationships_with_additional_fields(self, http_session, base_url):
        """Test updating family relationships with additional fields."""
        player_id = "456"
        responses.add(
            responses.PATCH,
            f"{base_url}/players/{player_id}/family-relationships",
            json={"updated": True, "notification_sent": True},
            status=200
        )

        players = PlayersEndpoint(http_session)
        response = players.update_family_relationships(
            player_id=player_id,
            action="add", 
            entities=["newparent@example.com"],
            additional_fields={
                "notification_preference": "email",
                "access_level": "view_only"
            },
            send_welcome_email=True
        )
        
        assert response["updated"] is True


class TestSearchEndpoint:
    """Test the SearchEndpoint class with hybrid approach functionality."""

    @responses.activate
    def test_search_basic(self, http_session, base_url):
        """Test basic search functionality."""
        responses.add(
            responses.POST,
            f"{base_url}/search",
            json={"results": [{"id": "1", "name": "Test Team", "type": "team"}]},
            status=200
        )

        search = SearchEndpoint(http_session)
        response = search.search(name="Test Team")
        
        assert len(response["results"]) == 1
        assert response["results"][0]["name"] == "Test Team"

    @responses.activate
    def test_search_with_parameters(self, http_session, base_url):
        """Test search with typed parameters."""
        responses.add(
            responses.POST,
            f"{base_url}/search",
            json={"results": [{"id": "2", "name": "Baseball Team", "type": "team"}]},
            status=200
        )

        search = SearchEndpoint(http_session)
        response = search.search(
            name="Baseball Team",
            types=["team"],
            sport="baseball",
            states=["GA", "FL"]
        )
        
        assert response["results"][0]["name"] == "Baseball Team"

    @responses.activate
    def test_search_with_seasons(self, http_session, base_url):
        """Test search with season objects."""
        responses.add(
            responses.POST,
            f"{base_url}/search", 
            json={"results": [{"id": "3", "name": "Spring Team", "type": "team"}]},
            status=200
        )

        search = SearchEndpoint(http_session)
        seasons = [
            SearchEndpoint.create_season("spring", 2025),
            SearchEndpoint.create_season("summer", 2025)
        ]
        
        response = search.search(
            name="Spring Team",
            seasons=seasons,
            types=["team"]
        )
        
        assert response["results"][0]["name"] == "Spring Team"

    @responses.activate
    def test_search_with_coordinates(self, http_session, base_url):
        """Test search with coordinates."""
        responses.add(
            responses.POST,
            f"{base_url}/search",
            json={"results": [{"id": "4", "name": "Atlanta Team", "type": "team"}]},
            status=200
        )

        search = SearchEndpoint(http_session)
        coords = SearchEndpoint.create_coordinates(33.7490, -84.3880)
        
        response = search.search(
            name="Atlanta Team",
            coordinates=coords,
            types=["team"]
        )
        
        assert response["results"][0]["name"] == "Atlanta Team"

    @responses.activate
    def test_search_with_additional_fields(self, http_session, base_url):
        """Test search with additional fields."""
        responses.add(
            responses.POST,
            f"{base_url}/search",
            json={"results": [{"id": "5", "name": "Advanced Team", "type": "team"}]},
            status=200
        )

        search = SearchEndpoint(http_session)
        response = search.search(
            name="Advanced Team",
            types=["team"],
            additional_fields={
                "advanced_filter": True,
                "sort_by": "relevance"
            },
            include_inactive=False
        )
        
        assert response["results"][0]["name"] == "Advanced Team"

    def test_create_season_helper(self):
        """Test the create_season helper method."""
        season = SearchEndpoint.create_season("spring", 2025)
        assert season == {"name": "spring", "year": 2025}

    def test_create_season_invalid_name(self):
        """Test create_season with invalid season name."""
        with pytest.raises(ValueError) as exc_info:
            SearchEndpoint.create_season("invalid", 2025)
        
        assert "Season name must be one of" in str(exc_info.value)

    def test_create_coordinates_helper(self):
        """Test the create_coordinates helper method."""
        coords = SearchEndpoint.create_coordinates(33.7490, -84.3880)
        assert coords == {"lat": 33.7490, "long": -84.3880}


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
