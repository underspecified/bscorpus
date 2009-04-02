<x:stylesheet version="1.0"
	xmlns:x="http://www.w3.org/1999/XSL/Transform" 
	xmlns:idx="urn:atom-extension:indexing"
	xmlns:gr="http://www.google.com/schemas/reader/atom/"
	xmlns:media="http://search.yahoo.com/mrss/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	idx:index="no">

<x:template match="//atom:entry">
ENTRY\t<x:value-of select="atom:source/atom:title"/>\t<x:value-of select="atom:title"/>\t<x:value-of select="atom:link/@href"/>
<x:for-each select="atom:category">
CATEGORY\t<x:value-of select="@term"/>
</x:for-each>
</x:template>

</x:stylesheet>
