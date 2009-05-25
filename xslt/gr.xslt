<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:idx="urn:atom-extension:indexing"
 xmlns:gr="http://www.google.com/schemas/reader/atom/"
 xmlns:media="http://search.yahoo.com/mrss/"
 xmlns:atom="http://www.w3.org/2005/Atom"
 idx:index="no">

<xsl:output method="text"/>
<xsl:strip-space elements="*"/>

<xsl:template match="/atom:feed/atom:entry">
	<!-- the blog's title -->
	<xsl:value-of select="atom:source/atom:title"/>
	<xsl:text>&#xa;</xsl:text>
	
	<!-- the post's title -->
	<xsl:value-of select="atom:title"/>
	<xsl:text>&#xa;</xsl:text>
	
	<!-- the post's url -->
	<xsl:value-of select="atom:link/@href"/>
	<xsl:text>&#xa;</xsl:text>

	<!-- the post's categories -->
	<xsl:for-each select="atom:category">
		<xsl:value-of select="@term"/>
		<xsl:text>&#xa;</xsl:text>
	</xsl:for-each>
	
	<xsl:text>&#xa;</xsl:text>
</xsl:template>

<!-- block entries we are uninterested in -->
<xsl:template match="*[not(self::atom:feed)]">
</xsl:template>

</xsl:stylesheet>
